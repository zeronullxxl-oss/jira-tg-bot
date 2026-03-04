import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://localhost:8080")

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "PROJ")
JIRA_PROJECT_KEYS = [k.strip() for k in os.getenv("JIRA_PROJECT_KEYS", JIRA_PROJECT_KEY).split(",")]

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8080))
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "changeme")

STATUS_MAP = {
    "To Do": {"label": "To Do", "color": "#6b7280", "order": 0},
    "Backlog": {"label": "Backlog", "color": "#6b7280", "order": 0},
    "Selected for Design": {"label": "Selected", "color": "#a78bfa", "order": 1},
    "Selected for Development": {"label": "Selected", "color": "#a78bfa", "order": 1},
    "Ready for Development": {"label": "Ready for Dev", "color": "#eab308", "order": 2},
    "Ready for Design": {"label": "Ready for Design", "color": "#eab308", "order": 2},
    "In Progress": {"label": "In Progress", "color": "#3b82f6", "order": 3},
    "In Design": {"label": "In Design", "color": "#8b5cf6", "order": 3},
    "Ready to Test": {"label": "Ready to Test", "color": "#f59e0b", "order": 4},
    "In Review": {"label": "Review", "color": "#f97316", "order": 5},
    "Revision": {"label": "Revision", "color": "#ef4444", "order": 5},
    "Ready to Buyer Review": {"label": "Buyer Review", "color": "#ec4899", "order": 6},
    "In QA": {"label": "QA", "color": "#f97316", "order": 5},
    "Published": {"label": "Published", "color": "#22c55e", "order": 7},
    "Done": {"label": "Done", "color": "#22c55e", "order": 7},
    "Closed": {"label": "Closed", "color": "#22c55e", "order": 7},
}
