from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from services.favourites import add_city, remove_city, get_user_city
from services.keyboards import create_action_keyboard, create_cities_keyboard
from services.weather_api import get_weather_by_city
from services.weather_formatter import send_weather_report

favourites_router = Router()

@favourites_router.message(Command('add_city'))
async def process_command_add_city(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer('❌ Использование: /add_city (название_города)\nПример: /add_city Москва')
        return

    city = args[1].split()
    user_id = message.from_user.id

    if add_city(user_id, city):
        await message.answer(f'Город {city} добавлен в избранное')
    else:
        await message.answer(f'Город {city} уже находится в избранном')

@favourites_router.message(Command('my_cities'))
async def process_command_my_cities(message: Message):
    user_id = message.from_user.id
    cities = get_user_city(user_id)

    if not cities:
        await message.answer('У вас пока нет городов в списке избранных')
        return

    cities_list = '\n'.join([f'{city}' for city in cities])
    text = f'Ваши избранные города:\n{cities_list}'

    keyboard = create_cities_keyboard(cities)

    await message.answer(text, reply_markup=keyboard)

@favourites_router.message(Command('remove_city'))
async def process_command_removeCity(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer('❌ Использование: /remove_city (название_города)\nПример: /remove_city Москва')
        return

    city = args[1].strip()
    user_id = message.from_user.id

    if remove_city(user_id, city):
        await message.answer(f'Город: {city} успешно удален из списка избранных')
    else:
        await message.answer(f'Город: {city} не найден в вашем списке!')

@favourites_router.callback_query(F.data.startswith('city:'))
async def process_city_selection(callback: CallbackQuery):
    action, city = callback.data.split(':', 1)

    keyboard = create_action_keyboard(city)

    await callback.message.edit_text(
        f'Вы выбрали город: <b>{city}</b>\n Что хотите сделать?',
        reply_markup=keyboard
    )

    await callback.answer()

@favourites_router.callback_query(F.data.startswith('weather:'))
async def process_show_weather(callback: CallbackQuery):
    action, city = callback.data.split(':', 1)

    await callback.message.edit_text(
        f'Загружую погоду для города <b>{city}</b>'
    )
    await callback.answer()

    await send_weather_report(callback, city)


@favourites_router.callback_query(F.data.startswith('remove:'))
async def process_remove_city(callback: CallbackQuery):
    action, city = callback.data.split(':', 1)
    user_id = callback.from_user.id

    remove_city(user_id, city)

    cities = get_user_city(user_id)

    if cities:
        keyboard = create_cities_keyboard(cities)
        await callback.message.edit_text(
            f'Город {city} удален.\n\nВаши избранные города',
            reply_markup=keyboard
        )
    else:
        await callback.messag.edit_text('Город удален.  Список избранного пуст')
    await callback.answer(f'Город {city} удален')

@favourites_router.callback_query(F.data == 'back_to_cities')
async def process_back_to_cities(callback: CallbackQuery):
    user_id = callback.from_user_id
    cities = get_user_city(user_id)

    if cities:
        keyboard = create_cities_keyboard(cities)
        await callback.message.edit_text(
            f'Ваши избранные города', reply_markup=keyboard
        )
    else:
        await callback.message.edit_text('Список избранного пуст')

    await callback.answer()