import asyncpg
from config import DATABASE_URL

pool: asyncpg.Pool | None = None

async def init_pool():
    global pool
    pool = await asyncpg.create_pool(dsn=DATABASE_URL, min_size=2, max_size=10)

async def close_pool():
    global pool 
    if pool:
        await pool.close()

async def get_user_cities(user_id: int) -> list[str]:
    rows = await pool.fetch(
        """
        SELECT c.name
        FROM favorites f
        JOIN cities c ON c.id = f.city_id
        WHERE f.user_id=$1
        ORDER BY c.name
        """,
        user_id
    )
    return [row['name'] for row in rows]