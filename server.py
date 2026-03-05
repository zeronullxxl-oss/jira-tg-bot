import asyncio
import hashlib
import hmac
import json
import logging
import os
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, MenuButtonWebApp, WebAppInfo
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, WEBAPP_URL, HOST, PORT, WEBHOOK_SECRET, STATUS_MAP, JIRA_URL
from database import init_db, add_user, get_user_profile, save_user_profile, DATABASE_URL, USE_PG
from templates import TEMPLATES, TEAMS, build_summary, build_description, build_adf_description
from telegraph_client import publish_page as telegraph_publish

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server")

# ── Mock mode: if Jira creds are empty, skip Jira calls ─────────────
MOCK_MODE = not JIRA_URL or JIRA_URL == "https://your-domain.atlassian.net"
if MOCK_MODE:
    logger.warning("=== MOCK MODE: Jira disabled ===")

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

_mock_counter = 0
_mock_tasks = []  # in-memory mock storage for dev mode


def validate_init_data(init_data_raw):
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


async def api_get_profile(request):
    init_data = request.headers.get("X-Telegram-Init-Data", "")
    user = validate_init_data(init_data)
    if not user:
        return web.json_response({"error": "Unauthorized"}, status=401)
    tg_id = user["id"]
    await add_user(tg_id, user.get("username"), user.get("first_name"))
    profile = await get_user_profile(tg_id)
    if profile and profile.get("buyer_name") and profile.get("buyer_tag") and profile.get("jira_email") and profile.get("jira_token"):
        safe_profile = {k: v for k, v in profile.items() if k != "jira_token"}
        safe_profile["has_jira"] = True
        return web.json_response({"registered": True, **safe_profile})
    return web.json_response({"registered": False, "tg_id": tg_id})


async def api_save_profile(request):
    init_data = request.headers.get("X-Telegram-Init-Data", "")
    user = validate_init_data(init_data)
    if not user:
        return web.json_response({"error": "Unauthorized"}, status=401)
    body = await request.json()
    buyer_name = body.get("buyer_name", "").strip()
    buyer_tag = body.get("buyer_tag", "").strip()
    jira_email = body.get("jira_email", "").strip()
    jira_token = body.get("jira_token", "").strip()
    if not buyer_name or not buyer_tag or not jira_email or not jira_token:
        return web.json_response({"error": "All fields required"}, status=400)
    await save_user_profile(
        user["id"], buyer_name, buyer_tag, jira_email, jira_token,
        user.get("username"), user.get("first_name"),
    )
    return web.json_response({"ok": True})


async def api_get_templates(request):
    result = {"teams": TEAMS, "templates": TEMPLATES}
    return web.json_response(result, dumps=lambda x: json.dumps(x, ensure_ascii=False))


async def api_get_tasks(request):
    """Fetch tasks from Jira by Buyer Tag. Mock mode uses in-memory list."""
    init_data = request.headers.get("X-Telegram-Init-Data", "")
    user = validate_init_data(init_data)
    if not user:
        return web.json_response({"error": "Unauthorized"}, status=401)
    tg_id = user["id"]
    profile = await get_user_profile(tg_id)
    buyer_tag = profile.get("buyer_tag", "") if profile else ""

    if MOCK_MODE:
        result = []
        for t in _mock_tasks:
            if t["tg_id"] == tg_id:
                si = STATUS_MAP.get(t["status"], {"label": t["status"], "color": "#6b7280", "order": 99})
                result.append({
                    "jira_key": t["jira_key"], "summary": t["summary"],
                    "status": t["status"], "status_label": si["label"],
                    "status_color": si["color"], "status_order": si["order"],
                    "created_at": t["created_at"], "jira_url": "#",
                })
        return web.json_response(result)

    if not buyer_tag:
        logger.warning("No buyer_tag for tg_id=%s", tg_id)
        return web.json_response([])

    jira_email = profile.get("jira_email", "") if profile else ""
    jira_token = profile.get("jira_token", "") if profile else ""
    if not jira_email or not jira_token:
        return web.json_response([])

    logger.info("Fetching tasks for buyer_tag='%s' tg_id=%s", buyer_tag, tg_id)
    try:
        from jira_client import search_issues
        res = await search_issues(jira_email, jira_token, buyer_tag)
        if "error" in res:
            return web.json_response({"error": res["error"]}, status=400)
        result = []
        for issue in res.get("issues", []):
            status_name = issue["status"]
            si = STATUS_MAP.get(status_name, {"label": status_name, "color": "#6b7280", "order": 99})
            result.append({
                "jira_key": issue["jira_key"],
                "summary": issue["summary"],
                "status": status_name,
                "status_label": si["label"],
                "status_color": si["color"],
                "status_order": si["order"],
                "project": issue.get("project", ""),
                "priority": issue.get("priority", ""),
                "created_at": issue["created_at"],
                "jira_url": issue["jira_url"],
            })
        return web.json_response(result)
    except Exception as e:
        logger.error("Jira fetch error: %s", e)
        return web.json_response({"error": str(e)}, status=500)


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
    profile = await get_user_profile(tg_id)
    buyer_name = profile.get("buyer_name", "Unknown") if profile else "Unknown"
    buyer_tag = profile.get("buyer_tag", "") if profile else ""
    summary = build_summary(template_key, data)
    description = build_description(template_key, data)
    adf_nodes = build_adf_description(template_key, data, buyer_name=profile.get("buyer_name", ""), buyer_tag=buyer_tag)
    description = f"Buyer: {buyer_name} ({buyer_tag})\n{description}"

    # Auto-publish telegraph text if provided
    telegraph_text = data.get("telegraph_text", "").strip()
    if telegraph_text:
        try:
            tg_url = await telegraph_publish(summary, telegraph_text)
            if tg_url:
                description += f"\n\nTelegraph: {tg_url}"
                logger.info("Telegraph published: %s", tg_url)
        except Exception as e:
            logger.error("Telegraph publish failed: %s", e)

    if MOCK_MODE:
        global _mock_counter
        _mock_counter += 1
        jira_key = f"MOCK-{_mock_counter}"
        from datetime import datetime
        _mock_tasks.append({
            "tg_id": tg_id, "jira_key": jira_key, "summary": summary,
            "status": "To Do", "created_at": datetime.now().isoformat(),
        })
        logger.info("MOCK task: %s - %s", jira_key, summary)
        logger.info("Description:\n%s", description)
        return web.json_response({
            "ok": True, "jira_key": jira_key,
            "summary": summary, "jira_url": "#",
        })
    else:
        try:
            from jira_client import create_issue, attach_file
            jira_email = profile.get("jira_email", "")
            jira_token = profile.get("jira_token", "")
            if not jira_email or not jira_token:
                return web.json_response({"error": "Jira credentials missing"}, status=400)
            result = await create_issue(
                jira_email, jira_token,
                summary=summary, description=description,
                buyer_tag=buyer_tag,
                project_key=TEAMS.get(TEMPLATES[template_key]["team"], {}).get("project"),
                adf_content=adf_nodes,
            )
            if "error" in result:
                return web.json_response({"error": result["error"]}, status=400)
            jira_key = result["key"]

            for fpath, fname in uploaded_files:
                try:
                    await attach_file(jira_email, jira_token, jira_key, fpath, fname)
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


async def api_get_statuses(request):
    return web.json_response(STATUS_MAP)


async def api_logout(request):
    """Reset user profile — back to registration."""
    init_data = request.headers.get("X-Telegram-Init-Data", "")
    user = validate_init_data(init_data)
    if not user:
        return web.json_response({"error": "Unauthorized"}, status=401)
    tg_id = user["id"]
    if USE_PG:
        import asyncpg
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            await conn.execute(
                "UPDATE users SET buyer_name=NULL, buyer_tag=NULL, jira_email=NULL, jira_token=NULL WHERE tg_id=$1",
                tg_id,
            )
        finally:
            await conn.close()
    else:
        import aiosqlite
        db_path = os.path.join(os.path.dirname(__file__), "bot.db")
        async with aiosqlite.connect(db_path) as db:
            await db.execute(
                "UPDATE users SET buyer_name=NULL, buyer_tag=NULL, jira_email=NULL, jira_token=NULL WHERE tg_id=?",
                (tg_id,),
            )
            await db.commit()
    logger.info("User %s logged out", tg_id)
    return web.json_response({"ok": True})


async def api_update_status(request):
    """Move task to a new status via Jira transitions."""
    init_data = request.headers.get("X-Telegram-Init-Data", "")
    user = validate_init_data(init_data)
    if not user:
        return web.json_response({"error": "Unauthorized"}, status=401)
    tg_id = user["id"]
    profile = await get_user_profile(tg_id)
    jira_email = profile.get("jira_email", "") if profile else ""
    jira_token = profile.get("jira_token", "") if profile else ""
    if not jira_email or not jira_token:
        return web.json_response({"error": "Jira credentials missing"}, status=400)

    body = await request.json()
    issue_key = body.get("jira_key")
    transition_id = body.get("transition_id")
    if not issue_key or not transition_id:
        return web.json_response({"error": "Missing jira_key or transition_id"}, status=400)

    from jira_client import do_transition
    result = await do_transition(jira_email, jira_token, issue_key, transition_id)
    if "error" in result:
        return web.json_response(result, status=400)
    logger.info("Transition %s on %s by tg_id=%s", transition_id, issue_key, tg_id)
    return web.json_response({"ok": True})


async def api_get_transitions(request):
    """Get available transitions for a task."""
    init_data = request.headers.get("X-Telegram-Init-Data", "")
    user = validate_init_data(init_data)
    if not user:
        return web.json_response({"error": "Unauthorized"}, status=401)
    tg_id = user["id"]
    profile = await get_user_profile(tg_id)
    jira_email = profile.get("jira_email", "") if profile else ""
    jira_token = profile.get("jira_token", "") if profile else ""
    if not jira_email or not jira_token:
        return web.json_response({"error": "Jira credentials missing"}, status=400)

    issue_key = request.query.get("key", "")
    if not issue_key:
        return web.json_response({"error": "Missing key"}, status=400)

    from jira_client import get_transitions
    transitions = await get_transitions(jira_email, jira_token, issue_key)

    # Filter: only allowed buyer transitions
    ALLOWED_MOVES = {
        "To Do": ["Ready for Development"],
        "Ready to Buyer Review": ["Published"],
    }
    # Get current status from query param
    current_status = request.query.get("status", "")
    allowed_targets = ALLOWED_MOVES.get(current_status, [])
    filtered = [t for t in transitions if t["to"] in allowed_targets] if allowed_targets else []

    return web.json_response(filtered)


async def jira_webhook(request):
    """Jira webhook — notify buyer about status change."""
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

    # Extract tg_id from labels
    labels = issue.get("fields", {}).get("labels", [])
    tg_id = None
    for lbl in labels:
        if lbl.startswith("tg_"):
            try:
                tg_id = int(lbl[3:])
            except ValueError:
                pass
            break

    if not tg_id or not bot:
        return web.Response(status=200)

    changelog = payload.get("changelog", {})
    for item in changelog.get("items", []):
        if item.get("field") == "status":
            new_status = item.get("toString")
            old_status = item.get("fromString")
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
    app.router.add_get("/api/profile", api_get_profile)
    app.router.add_post("/api/profile", api_save_profile)
    app.router.add_get("/api/templates", api_get_templates)
    app.router.add_get("/api/tasks", api_get_tasks)
    app.router.add_post("/api/tasks", api_create_task)
    app.router.add_get("/api/statuses", api_get_statuses)
    app.router.add_post("/api/tasks/status", api_update_status)
    app.router.add_get("/api/tasks/transitions", api_get_transitions)
    app.router.add_post("/api/logout", api_logout)
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
        try:
            while True:
                await asyncio.sleep(3600)
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        finally:
            await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
