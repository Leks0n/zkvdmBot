import asyncio
from asyncpg import ForeignKeyViolationError, pool

import services.database as db
from services.database import (get_user_cities, init_pool, close_pool, add_city, remove_city, ensure_user)

async def cleanup():
    await db.pool.execute(
        """
        DELETE FROM favorites WHERE user_id IN (555000111, 777000333);
        """
    )
    await db.pool.execute(
        """
        DELETE FROM users WHERE user_id IN (555000111, 777000333);
        """
    )
    await db.pool.execute(
        """
        DELETE FROM cities WHERE name IN ('Казань', 'Тула');
        """
    )

async def main():
    await init_pool()
    try:
        await cleanup()
        print(await ensure_user(555000111, None))
        print(await add_city(555000111, 'Казань'))
        await add_city(777000333, 'Тула')
    except ForeignKeyViolationError:
        print('FL violation: пользователь не существует')       
    finally:
        await close_pool()

if __name__ == '__main__':
    asyncio.run(main())

