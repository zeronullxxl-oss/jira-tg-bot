import asyncio
import hashlib
import hmac
import json
import logging
import os
import uuid
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, MenuButtonWebApp, WebAppInfo
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, WEBAPP_URL, HOST, PORT, WEBHOOK_SECRET, STATUS_MAP, JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN
from database import init_db, add_user, add_task, get_user_tasks, update_task_status
from templates import TEMPLATES, build_summary, build_description

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server")

# ── Mock mode: if Jira creds are empty, skip Jira calls ─────────────
MOCK_MODE = not JIRA_URL or not JIRA_API_TOKEN or JIRA_URL == "https://your-domain.atlassian.net"
if MOCK_MODE:
    logger.warning("=== MOCK MODE: Jira disabled, tasks saved locally ===")

bot = None
dp = None

BOT_ENABLED = BOT_TOKEN and BOT_TOKEN != "your_telegram_bot_token"
if BOT_ENABLED:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        await add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
        await bot.set_chat_menu_button(
            chat_id=message.chat.id,
            menu_button=MenuButtonWebApp(text="Open Tasks", web_app=WebAppInfo(url=WEBAPP_URL)),
        )
        await message.answer("Ready! Tap the menu button below to open task manager.")
else:
    logger.warning("=== BOT DISABLED: no BOT_TOKEN, running web only ===")


UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Counter for mock issue keys
_mock_counter = 0


def validate_init_data(init_data_raw):
    """Validate TG initData. In mock mode without bot, allow dev user."""
    if not init_data_raw and not BOT_ENABLED:
        return {"id": 12345678, "first_name": "Dev", "username": "dev"}
    if not init_data_raw:
        return None
    try:
        from urllib.parse import parse_qs, unquote
        parsed = parse_qs(init_data_raw, keep_blank_values=True)
        check_hash = parsed.get("hash", [""])[0]
        items = []
        for k, v in sorted(parsed.items()):
            if k != "hash":
                items.append(f"{k}={v[0]}")
        data_check_string = "\n".join(items)
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        computed = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        if computed != check_hash:
            if not BOT_ENABLED:
                user_json = parsed.get("user", [""])[0]
                if user_json:
                    return json.loads(unquote(user_json))
            return None
        user_json = parsed.get("user", [""])[0]
        if user_json:
            return json.loads(unquote(user_json))
        return None
    except Exception as e:
        logger.error("initData validation: %s", e)
        if not BOT_ENABLED:
            return {"id": 12345678, "first_name": "Dev", "username": "dev"}
        return None


async def api_get_templates(request):
    return web.json_response(TEMPLATES, dumps=lambda x: json.dumps(x, ensure_ascii=False))


async def api_get_tasks(request):
    init_data = request.headers.get("X-Telegram-Init-Data", "")
    user = validate_init_data(init_data)
    if not user:
        return web.json_response({"error": "Unauthorized"}, status=401)
    tg_id = user["id"]
    tasks = await get_user_tasks(tg_id)
    result = []
    for t in tasks:
        si = STATUS_MAP.get(t["status"], {"label": t["status"], "color": "#6b7280", "order": 99})
        jira_url = f"{JIRA_URL}/browse/{t['jira_key']}" if not MOCK_MODE else "#"
        result.append({
            "jira_key": t["jira_key"], "summary": t["summary"],
            "status": t["status"], "status_label": si["label"],
            "status_color": si["color"], "status_order": si["order"],
            "template": t["template"], "created_at": t["created_at"],
            "jira_url": jira_url,
        })
    return web.json_response(result)


async def api_create_task(request):
    init_data = request.headers.get("X-Telegram-Init-Data", "")
    user = validate_init_data(init_data)
    if not user:
        return web.json_response({"error": "Unauthorized"}, status=401)

    uploaded_files = []
    if request.content_type and "multipart" in request.content_type:
        reader = await request.multipart()
        data = {}
        template_key = None
        while True:
            part = await reader.next()
            if part is None:
                break
            name = part.name
            if name == "template":
                template_key = (await part.text()).strip()
            elif name == "data":
                data = json.loads(await part.text())
            elif name.startswith("file_"):
                filename = part.filename
                if filename:
                    fpath = os.path.join(UPLOAD_DIR, f"{user['id']}_{filename}")
                    with open(fpath, "wb") as f:
                        while True:
                            chunk = await part.read_chunk()
                            if not chunk:
                                break
                            f.write(chunk)
                    uploaded_files.append((fpath, filename))
    else:
        body = await request.json()
        template_key = body.get("template")
        data = body.get("data", {})

    if not template_key or template_key not in TEMPLATES:
        return web.json_response({"error": "Unknown template"}, status=400)

    tg_id = user["id"]
    summary = build_summary(template_key, data)
    description = build_description(template_key, data)

    if MOCK_MODE:
        global _mock_counter
        _mock_counter += 1
        jira_key = f"MOCK-{_mock_counter}"
        await add_task(tg_id, jira_key, template_key, summary)
        logger.info("MOCK task created: %s - %s", jira_key, summary)
        logger.info("Description:\n%s", description)
        if uploaded_files:
            for fpath, fname in uploaded_files:
                logger.info("File attached: %s (%s)", fname, fpath)
        return web.json_response({
            "ok": True, "jira_key": jira_key,
            "summary": summary, "jira_url": "#",
        })
    else:
        try:
            from jira_client import jira
            result = await jira.create_issue(
                summary=summary, description=description,
                labels=[f"tg_{tg_id}", "bot-created"],
            )
            jira_key = result["key"]
            await add_task(tg_id, jira_key, template_key, summary)

            for fpath, fname in uploaded_files:
                try:
                    await attach_file_to_jira(jira_key, fpath, fname)
                except Exception as e:
                    logger.error("File attach failed: %s", e)
                finally:
                    if os.path.exists(fpath):
                        os.remove(fpath)

            return web.json_response({
                "ok": True, "jira_key": jira_key,
                "summary": summary,
                "jira_url": f"{JIRA_URL}/browse/{jira_key}",
            })
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)


async def attach_file_to_jira(issue_key, filepath, filename):
    import aiohttp
    from aiohttp import FormData
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/attachments"
    auth = aiohttp.BasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {"X-Atlassian-Token": "no-check"}
    data = FormData()
    data.add_field("file", open(filepath, "rb"), filename=filename)
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.post(url, headers=headers, data=data) as resp:
            if resp.status >= 400:
                text = await resp.text()
                logger.error("Jira attach error %s: %s", resp.status, text)


async def api_get_statuses(request):
    return web.json_response(STATUS_MAP)


async def api_update_status(request):
    """Manual status update for testing in mock mode."""
    if not MOCK_MODE:
        return web.json_response({"error": "Only in mock mode"}, status=403)
    body = await request.json()
    jira_key = body.get("jira_key")
    new_status = body.get("status")
    if not jira_key or not new_status:
        return web.json_response({"error": "Missing jira_key or status"}, status=400)
    tg_id = await update_task_status(jira_key, new_status)
    return web.json_response({"ok": True, "tg_id": tg_id})


async def jira_webhook(request):
    secret = request.query.get("secret", "")
    if secret != WEBHOOK_SECRET:
        return web.Response(status=403)
    try:
        payload = await request.json()
    except Exception:
        return web.Response(status=400)
    if payload.get("webhookEvent") != "jira:issue_updated":
        return web.Response(status=200)
    issue = payload.get("issue", {})
    jira_key = issue.get("key")
    if not jira_key:
        return web.Response(status=200)
    changelog = payload.get("changelog", {})
    for item in changelog.get("items", []):
        if item.get("field") == "status":
            new_status = item.get("toString")
            old_status = item.get("fromString")
            tg_id = await update_task_status(jira_key, new_status)
            if tg_id and bot:
                old_info = STATUS_MAP.get(old_status, {"label": old_status})
                new_info = STATUS_MAP.get(new_status, {"label": new_status})
                summary = issue.get("fields", {}).get("summary", "")
                try:
                    text = f"Task updated!\n\n{jira_key}\n{summary}\n\n{old_info['label']} -> {new_info['label']}"
                    await bot.send_message(tg_id, text)
                except Exception as e:
                    logger.error("Notify failed %s: %s", tg_id, e)
            break
    return web.Response(status=200)


async def main():
    await init_db()
    app = web.Application(client_max_size=50 * 1024 * 1024)
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    app.router.add_static("/static", static_dir)

    async def index(request):
        return web.FileResponse(os.path.join(static_dir, "index.html"))

    app.router.add_get("/", index)
    app.router.add_get("/health", lambda r: web.Response(text="OK"))
    app.router.add_get("/api/templates", api_get_templates)
    app.router.add_get("/api/tasks", api_get_tasks)
    app.router.add_post("/api/tasks", api_create_task)
    app.router.add_get("/api/statuses", api_get_statuses)
    app.router.add_post("/api/tasks/status", api_update_status)
    app.router.add_post("/webhook/jira", jira_webhook)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, HOST, PORT)

    logger.info("=" * 50)
    logger.info("Server on http://%s:%s", HOST, PORT)
    if MOCK_MODE:
        logger.info("MOCK MODE: open http://localhost:%s in browser", PORT)
    logger.info("=" * 50)

    await site.start()

    if dp and bot:
        try:
            await dp.start_polling(bot)
        finally:
            await runner.cleanup()
            await bot.session.close()
    else:
        # No bot - just run web server
        try:
            while True:
                await asyncio.sleep(3600)
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        finally:
            await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
