from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .utils import clean_city_name

def create_cities_keyboard(cities: list) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    print(f'===ОТЛАДКА cities = {cities}')
    print(f'===ОТЛАДКА cities = {type(cities)}')

    for city in cities:
        print(f"=== ОТЛАДКА: city = {city}, тип = {type(city)}")

        city_name = clean_city_name(city)

        if not city_name:
            continue

        builder.button(text=city, callback_data=f'city:{city_name}')

    builder.adjust(2)

    return builder.as_markup()

def create_action_keyboard(city: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    city_name = clean_city_name(city)

    builder.button(text='Показать погоду', callback_data=f'weather:{city_name}')
    builder.button(text='Удалить из избранного', callback_data=f'remove:{city_name}')

    builder.adjust(1)

    return builder.as_markup()