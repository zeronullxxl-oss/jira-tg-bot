# Jira Task Bot - Telegram Mini App

Mini App for buyers to create Jira tasks and track status.

## Setup

1. pip install -r requirements.txt
2. cp .env.example .env and fill in values
3. Get Jira API token from id.atlassian.com
4. Setup Jira webhook: /webhook/jira?secret=SECRET
5. python server.py

## Files

- server.py - entry point (bot + API + static)
- config.py - env settings
- jira_client.py - Jira REST API
- database.py - SQLite
- templates.py - task templates
- static/index.html - Mini App React frontend
