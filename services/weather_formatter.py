from aiogram.types import Message, CallbackQuery

from .weather_api import get_weather_by_city

async def send_weather_report(message: Message | CallbackQuery, city: str):
    weather_data = await get_weather_by_city(city)

    if not weather_data:
        response_text= f'Город {city} не найден'
    else:
        response_text=(
            f'🌍 <b>{weather_data['city']}</b>\n\n'
            f'Температура: {weather_data['temperature']}°C\n'
            f'Ветер: {weather_data['windspeed']} м/с\n'
            f'{weather_data['description']}\n'
            f'УФ: {weather_data['uv_description']}'
        )

    if isinstance(message, CallbackQuery):
        await message.message.edit_text(response_text, parse_mode='HTML')
        await message.answer()
    else:
        await message.answer(response_text, parse_mode='HTML')