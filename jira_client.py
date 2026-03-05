import aiohttp
import json
import logging

from config import JIRA_URL, JIRA_PROJECT_KEYS

logger = logging.getLogger("jira")

BUYER_TAG_FIELD = "customfield_10059"


async def search_issues(jira_email, jira_token, buyer_tag):
    """Fetch issues by Buyer Tag using user's own Jira credentials."""
    base = JIRA_URL.rstrip("/")
    url = f"{base}/rest/api/3/search/jql"
    auth = aiohttp.BasicAuth(jira_email, jira_token)
    projects = ", ".join([f'"{k}"' for k in JIRA_PROJECT_KEYS])
    jql = f'project in ({projects}) AND "Buyer Tag" = "{buyer_tag}" ORDER BY created DESC'
    params = {
        "jql": jql,
        "maxResults": 50,
        "fields": "summary,status,created,priority,project",
    }
    logger.info("Jira search JQL: %s (user: %s)", jql, jira_email)
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(url, headers={"Accept": "application/json"}, params=params) as resp:
            data = await resp.json()
            logger.info("Jira response status=%s total=%s", resp.status, data.get("total", "N/A"))
            if resp.status == 401:
                logger.error("Jira auth failed for %s", jira_email)
                return {"error": "Неверный email или API токен Jira"}
            if resp.status >= 400:
                logger.error("Search error %s: %s", resp.status, data)
                return {"error": f"Jira error: {resp.status}"}
            issues = []
            for item in data.get("issues", []):
                fields = item.get("fields", {})
                status_name = fields.get("status", {}).get("name", "To Do")
                status_cat = fields.get("status", {}).get("statusCategory", {}).get("key", "new")
                project_key = fields.get("project", {}).get("key", "")
                priority_name = fields.get("priority", {}).get("name", "")
                issues.append({
                    "jira_key": item["key"],
                    "summary": fields.get("summary", ""),
                    "status": status_name,
                    "status_category": status_cat,
                    "project": project_key,
                    "priority": priority_name,
                    "created_at": fields.get("created", ""),
                    "jira_url": f"{base}/browse/{item['key']}",
                })
            return {"issues": issues}


async def create_issue(jira_email, jira_token, summary, description, buyer_tag=None, project_key=None, adf_content=None):
    """Create issue using user's own Jira credentials."""
    base = JIRA_URL.rstrip("/")
    url = f"{base}/rest/api/3/issue"
    auth = aiohttp.BasicAuth(jira_email, jira_token)
    proj = project_key or JIRA_PROJECT_KEYS[0]
    if adf_content:
        doc = {"version": 1, "type": "doc", "content": adf_content}
    else:
        nodes = []
        for line in description.split("\n"):
            nodes.append({
                "type": "paragraph",
                "content": [{"type": "text", "text": line}] if line.strip() else [],
            })
        doc = {"version": 1, "type": "doc", "content": nodes}
    fields = {
        "project": {"key": proj},
        "summary": summary,
        "issuetype": {"name": "Story"},
        "description": doc,
        "labels": ["bot-created"],
    }
    if buyer_tag:
        fields[BUYER_TAG_FIELD] = {"value": buyer_tag}
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.post(url, headers={"Content-Type": "application/json"}, json={"fields": fields}) as resp:
            data = await resp.json()
            if resp.status == 401:
                return {"error": "Неверный email или API токен Jira"}
            if resp.status >= 400:
                logger.error("Create error %s: %s", resp.status, data)
                return {"error": f"Jira error: {data}"}
            return data


async def attach_file(jira_email, jira_token, issue_key, filepath, filename):
    base = JIRA_URL.rstrip("/")
    url = f"{base}/rest/api/3/issue/{issue_key}/attachments"
    auth = aiohttp.BasicAuth(jira_email, jira_token)
    headers = {"X-Atlassian-Token": "no-check"}
    data = aiohttp.FormData()
    data.add_field("file", open(filepath, "rb"), filename=filename)
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.post(url, headers=headers, data=data) as resp:
            if resp.status >= 400:
                text = await resp.text()
                logger.error("Attach error %s: %s", resp.status, text)
