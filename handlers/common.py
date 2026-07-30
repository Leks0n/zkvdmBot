from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from services.weather_api import get_weather_by_city

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
    )

@common_router.message(F.text)
async def process_city_message(message: Message):
    await message.answer(
        f'Ищу погоду в городе {message.text}'
    )

    weather_data = await get_weather_by_city(message.text)

    if weather_data:
        response = (
            f'🌍 <b>{weather_data['city']}</b>\n\n'
            f'Температура: {weather_data['temperature']}°C\n'
            f'Ветер: {weather_data['windspeed']} м/с\n'
            f'{weather_data['description']}\n'
            f'УФ: {weather_data['uv_description']}'
        )
        await message.answer(response)

    else:
        await message.answer(
            'Город не найден\n'
            'Попробуйте написать название на английском'
        )
