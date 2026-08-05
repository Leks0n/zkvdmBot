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
    pool = None

async def ensure_user(user_id: int, user_name: str | None) -> None:
    await pool.execute(
        """
        INSERT INTO users (user_id, username) VALUES ($1, $2)
        ON CONFLICT (user_id) DO UPDATE SET username = EXCLUDED.username
        """,
        user_id,
        user_name
    )


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

async def add_city(user_id: int, city_name: str) -> bool:
    await pool.execute(
        """
        INSERT INTO cities (name) VALUES ($1)
        ON CONFLICT (name) DO NOTHING
        """, 
        city_name                                                                                                 
    )

    city_id = await pool.fetchval(
        """
        SELECT id FROM cities WHERE name=$1
        """, 
        city_name
    )

    status = await pool.execute(
        """
        INSERT INTO favorites (user_id, city_id) VALUES ($1, $2)
        ON CONFLICT (user_id, city_id) DO NOTHING
        """,
        user_id,
        city_id,
    )

    return int(status.split()[-1]) == 1 

async def remove_city(user_id: int, city_name: str) -> bool: 
    city_id = await pool.fetchval(
        """
        SELECT id FROM cities WHERE name = $1
        """,
        city_name
    )
    if city_id is None:
        return False

    status = await pool.execute(
        """
        DELETE FROM favorites WHERE user_id = $1 AND city_id = $2
        """,
        user_id,
        city_id,
    )
    return int(status.split()[-1]) == 1

