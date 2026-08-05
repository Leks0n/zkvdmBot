import asyncio
from services.database import get_user_cities, init_pool, close_pool, add_city, remove_city

async def main():
    await init_pool()
    try:
        print(await get_user_cities(123456789))
        print(await get_user_cities(999999999))
        print(await add_city(123456789, 'Сочи'))
        print(await get_user_cities(123456789))
        print(await add_city(123456789, 'Сочи'))
        print(await remove_city(123456789, 'Сочи'))
        print(await remove_city(123456789, 'Сочи'))
        print(await get_user_cities(123456789))
        
    finally:
        await close_pool()

if __name__ == '__main__':
    asyncio.run(main())

