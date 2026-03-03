import aiohttp
import logging

logger = logging.getLogger("telegraph")

BASE_URL = "https://api.telegra.ph"
_token = None


async def _ensure_account():
    global _token
    if _token:
        return _token
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/createAccount", json={
            "short_name": "13Buyers",
            "author_name": "Task Manager",
        }) as resp:
            data = await resp.json()
            if data.get("ok"):
                _token = data["result"]["access_token"]
                logger.info("Telegraph account created")
                return _token
            else:
                logger.error("Telegraph createAccount failed: %s", data)
                return None


async def publish_page(title, text):
    """Publish text to telegra.ph. Returns URL or None."""
    token = await _ensure_account()
    if not token:
        return None

    # Convert plain text to Telegraph content nodes
    paragraphs = text.strip().split("\n")
    content = []
    for p in paragraphs:
        p = p.strip()
        if p:
            content.append({"tag": "p", "children": [p]})
        else:
            content.append({"tag": "br"})

    if not content:
        return None

    import json
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/createPage", json={
            "access_token": token,
            "title": title,
            "content": json.dumps(content),
            "author_name": "13Buyers",
        }) as resp:
            data = await resp.json()
            if data.get("ok"):
                url = data["result"]["url"]
                logger.info("Telegraph page created: %s", url)
                return url
            else:
                logger.error("Telegraph createPage failed: %s", data)
                return None
