import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://localhost:8080")

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "PROJ")

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8080))
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "changeme")

STATUS_MAP = {
    "To Do": {"label": "New", "color": "#6b7280", "order": 0},
    "Selected for Design": {"label": "Selected", "color": "#a78bfa", "order": 1},
    "Ready for Development": {"label": "Ready to Dev", "color": "#eab308", "order": 2},
    "In Progress": {"label": "In Progress", "color": "#3b82f6", "order": 3},
    "In Review": {"label": "On Review", "color": "#f97316", "order": 4},
    "Done": {"label": "Done", "color": "#22c55e", "order": 5},
}
