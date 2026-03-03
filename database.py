import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bot.db")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "tg_id INTEGER PRIMARY KEY, username TEXT, full_name TEXT, "
            "buyer_name TEXT, office TEXT, "
            "registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
        )
        await db.execute(
            "CREATE TABLE IF NOT EXISTS tasks ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "tg_id INTEGER NOT NULL, jira_key TEXT NOT NULL UNIQUE, "
            "template TEXT, status TEXT DEFAULT 'To Do', summary TEXT, "
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
            "FOREIGN KEY (tg_id) REFERENCES users(tg_id))"
        )
        # migrate: add columns if missing
        try:
            await db.execute("ALTER TABLE users ADD COLUMN buyer_name TEXT")
        except Exception:
            pass
        try:
            await db.execute("ALTER TABLE users ADD COLUMN office TEXT")
        except Exception:
            pass
        await db.commit()


async def add_user(tg_id, username=None, full_name=None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (tg_id, username, full_name) VALUES (?, ?, ?)",
            (tg_id, username, full_name),
        )
        await db.commit()


async def get_user_profile(tg_id):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT tg_id, username, full_name, buyer_name, office FROM users WHERE tg_id = ?",
            (tg_id,),
        )
        row = await cursor.fetchone()
        if row:
            return dict(row)
        return None


async def save_user_profile(tg_id, buyer_name, office, username=None, full_name=None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO users (tg_id, username, full_name, buyer_name, office) "
            "VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(tg_id) DO UPDATE SET buyer_name=?, office=?, username=?, full_name=?",
            (tg_id, username, full_name, buyer_name, office,
             buyer_name, office, username, full_name),
        )
        await db.commit()


async def add_task(tg_id, jira_key, template, summary, status="To Do"):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO tasks (tg_id, jira_key, template, summary, status) VALUES (?, ?, ?, ?, ?)",
            (tg_id, jira_key, template, summary, status),
        )
        await db.commit()


async def update_task_status(jira_key, new_status):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT tg_id FROM tasks WHERE jira_key = ?", (jira_key,)
        )
        row = await cursor.fetchone()
        if not row:
            return None
        await db.execute(
            "UPDATE tasks SET status = ? WHERE jira_key = ?",
            (new_status, jira_key)
        )
        await db.commit()
        return row[0]


async def get_user_tasks(tg_id):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT jira_key, template, status, summary, created_at "
            "FROM tasks WHERE tg_id = ? ORDER BY created_at DESC",
            (tg_id,),
        )
        return await cursor.fetchall()
