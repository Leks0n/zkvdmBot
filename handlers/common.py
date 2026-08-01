from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from services.weather_api import get_weather_by_city
from services.weather_formatter import send_weather_report

common_router = Router()

@common_router.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer('Привет, я бот для просмотра погоды ' \
    '\n\nНапиши название города, где ты хочешь уточнить погоду')

@common_router.message(Command('help'))
async def process_command_help(message: Message):
    await message.answer(
        "📖 <b>Как пользоваться:</b>\n\n"
        "1. Напиши название города (например: Москва)\n"
        "2. Я покажу текущую погоду\n"
        "3. Можешь уточнить город в любой момент\n\n"
        "Команды:\n"
        "/start - Начать работу\n"
        "/help - Показать справку"
        "/add_city (город) - Добавить в избранное\n"
        "/my_cities - Мои избранные города\n"
        "/remove_city (город) - Удалить из избранного"
    )

@common_router.message(F.text & ~F.text.startswith('/'))
async def process_city_message(message: Message):
    city_name = message.text.strip()

    await send_weather_report(message, city_name)
