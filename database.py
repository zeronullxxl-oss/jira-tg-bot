import os
import logging

logger = logging.getLogger("database")

DATABASE_URL = os.getenv("DATABASE_URL", "")
USE_PG = bool(DATABASE_URL)


async def _pg_execute(query, params=None, fetch=False, fetchone=False):
    import asyncpg
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        if fetch:
            rows = await conn.fetch(query, *(params or []))
            return [dict(r) for r in rows]
        elif fetchone:
            row = await conn.fetchrow(query, *(params or []))
            return dict(row) if row else None
        else:
            await conn.execute(query, *(params or []))
    finally:
        await conn.close()


async def init_db():
    if USE_PG:
        await _pg_execute("""
            CREATE TABLE IF NOT EXISTS users (
                tg_id BIGINT PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                buyer_name TEXT,
                buyer_tag TEXT,
                registered_at TIMESTAMP DEFAULT NOW()
            )
        """)
        # migration
        try:
            await _pg_execute("ALTER TABLE users ADD COLUMN buyer_tag TEXT")
        except Exception:
            pass
        logger.info("PostgreSQL ready")
    else:
        import aiosqlite
        db_path = os.path.join(os.path.dirname(__file__), "bot.db")
        async with aiosqlite.connect(db_path) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS users ("
                "tg_id INTEGER PRIMARY KEY, username TEXT, full_name TEXT, "
                "buyer_name TEXT, buyer_tag TEXT, "
                "registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
            )
            await db.commit()
        logger.info("SQLite ready")


async def add_user(tg_id, username=None, full_name=None):
    if USE_PG:
        await _pg_execute(
            "INSERT INTO users (tg_id, username, full_name) VALUES ($1, $2, $3) ON CONFLICT (tg_id) DO NOTHING",
            [tg_id, username, full_name],
        )
    else:
        import aiosqlite
        db_path = os.path.join(os.path.dirname(__file__), "bot.db")
        async with aiosqlite.connect(db_path) as db:
            await db.execute("INSERT OR IGNORE INTO users (tg_id, username, full_name) VALUES (?, ?, ?)", (tg_id, username, full_name))
            await db.commit()


async def get_user_profile(tg_id):
    if USE_PG:
        return await _pg_execute(
            "SELECT tg_id, username, full_name, buyer_name, buyer_tag FROM users WHERE tg_id = $1",
            [tg_id], fetchone=True,
        )
    else:
        import aiosqlite
        db_path = os.path.join(os.path.dirname(__file__), "bot.db")
        async with aiosqlite.connect(db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT tg_id, username, full_name, buyer_name, buyer_tag FROM users WHERE tg_id = ?", (tg_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None


async def save_user_profile(tg_id, buyer_name, buyer_tag, username=None, full_name=None):
    if USE_PG:
        await _pg_execute(
            "INSERT INTO users (tg_id, username, full_name, buyer_name, buyer_tag) VALUES ($1, $2, $3, $4, $5) "
            "ON CONFLICT (tg_id) DO UPDATE SET buyer_name=$4, buyer_tag=$5, username=$2, full_name=$3",
            [tg_id, username, full_name, buyer_name, buyer_tag],
        )
    else:
        import aiosqlite
        db_path = os.path.join(os.path.dirname(__file__), "bot.db")
        async with aiosqlite.connect(db_path) as db:
            await db.execute(
                "INSERT INTO users (tg_id, username, full_name, buyer_name, buyer_tag) VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(tg_id) DO UPDATE SET buyer_name=?, buyer_tag=?, username=?, full_name=?",
                (tg_id, username, full_name, buyer_name, buyer_tag, buyer_name, buyer_tag, username, full_name),
            )
            await db.commit()
