import aiohttp
from config import JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY


class JiraClient:
    def __init__(self):
        self.base_url = f"{JIRA_URL}/rest/api/3"
        self.auth = aiohttp.BasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    async def _request(self, method, endpoint, json_data=None):
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession(auth=self.auth, headers=self.headers) as session:
            async with session.request(method, url, json=json_data) as resp:
                if resp.status >= 400:
                    text = await resp.text()
                    raise Exception(f"Jira {resp.status}: {text}")
                if resp.status == 204:
                    return {}
                return await resp.json()

    async def create_issue(self, summary, description, labels=None, priority=None):
        fields = {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}],
            },
            "issuetype": {"name": "Task"},
        }
        if labels:
            fields["labels"] = labels
        if priority:
            fields["priority"] = {"name": priority}
        return await self._request("POST", "/issue", {"fields": fields})

    async def get_issues_by_label(self, label):
        jql = f'project = {JIRA_PROJECT_KEY} AND labels = "{label}" ORDER BY created DESC'
        result = await self._request(
            "GET", f"/search?jql={jql}&maxResults=50&fields=summary,status,priority,created,updated"
        )
        return result.get("issues", [])

    async def get_issue(self, key):
        return await self._request("GET", f"/issue/{key}")

    async def test_connection(self):
        try:
            await self._request("GET", "/myself")
            return True
        except Exception:
            return False


jira = JiraClient()
