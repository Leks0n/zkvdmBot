import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers.common import common_router
from handlers.favourites import favourites_router
from services.database import init_pool, close_pool

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    bot = Bot(
        token = BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    dp.include_router(favourites_router)
    dp.include_router(common_router)

    print('Запуск бота')
    await init_pool()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await close_pool()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен')