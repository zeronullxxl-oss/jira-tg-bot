import aiohttp
import json
import logging

from config import JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY, JIRA_PROJECT_KEYS

logger = logging.getLogger("jira")

BUYER_TAG_FIELD = "customfield_10059"


class JiraClient:
    def __init__(self):
        self.base = JIRA_URL.rstrip("/")
        self.auth = aiohttp.BasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

    async def create_issue(self, summary, description, labels=None, buyer_tag=None):
        url = f"{self.base}/rest/api/3/issue"
        # Build ADF description
        adf_content = []
        for line in description.split("\n"):
            adf_content.append({
                "type": "paragraph",
                "content": [{"type": "text", "text": line}] if line.strip() else [],
            })
        fields = {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "issuetype": {"name": "Story"},
            "description": {
                "version": 1,
                "type": "doc",
                "content": adf_content,
            },
        }
        if labels:
            fields["labels"] = labels
        if buyer_tag:
            fields[BUYER_TAG_FIELD] = {"value": buyer_tag}
        async with aiohttp.ClientSession(auth=self.auth) as session:
            async with session.post(
                url,
                headers={"Content-Type": "application/json"},
                json={"fields": fields},
            ) as resp:
                data = await resp.json()
                if resp.status >= 400:
                    logger.error("Create issue error %s: %s", resp.status, data)
                    raise Exception(f"Jira error: {data}")
                return data

    async def get_issues_by_buyer_tag(self, buyer_tag):
        """Fetch all issues with given Buyer Tag value across all projects."""
        url = f"{self.base}/rest/api/3/search/jql"
        projects = ", ".join([f'"{k}"' for k in JIRA_PROJECT_KEYS])
        jql = f'project in ({projects}) AND cf[10059] = "{buyer_tag}" ORDER BY created DESC'
        payload = {
            "jql": jql,
            "maxResults": 50,
            "fields": ["summary", "status", "created", "priority", "project"],
        }
        async with aiohttp.ClientSession(auth=self.auth) as session:
            async with session.post(url, headers={"Content-Type": "application/json", "Accept": "application/json"}, json=payload) as resp:
                data = await resp.json()
                if resp.status >= 400:
                    logger.error("Search error %s: %s", resp.status, data)
                    return []
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
                        "jira_url": f"{self.base}/browse/{item['key']}",
                    })
                return issues

    async def attach_file(self, issue_key, filepath, filename):
        url = f"{self.base}/rest/api/3/issue/{issue_key}/attachments"
        headers = {"X-Atlassian-Token": "no-check"}
        data = aiohttp.FormData()
        data.add_field("file", open(filepath, "rb"), filename=filename)
        async with aiohttp.ClientSession(auth=self.auth) as session:
            async with session.post(url, headers=headers, data=data) as resp:
                if resp.status >= 400:
                    text = await resp.text()
                    logger.error("Attach error %s: %s", resp.status, text)


jira = JiraClient()
