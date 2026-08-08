import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from asyncpg import PostgresError, InterfaceError

from services.database import add_city, remove_city, get_user_cities, ensure_user, DatabaseError
from services.keyboards import create_action_keyboard, create_cities_keyboard
from services.weather_formatter import send_weather_report
from services.utils import clean_city_name

logger = logging.getLogger(__name__)

favourites_router = Router()

@favourites_router.message(Command('add_city'))
async def process_command_add_city(message: Message):
    user_id = message.from_user.id
    
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer('❌ Использование: /add_city (название_города)\nПример: /add_city Москва')
        return

    city = clean_city_name(args[1])

    try:
        await ensure_user(user_id, message.from_user.username)
        if await add_city(user_id, city):
            await message.answer(f'Город {city} добавлен в избранное')
        else:
            await message.answer(f'Город {city} уже находится в избранном')
    except DatabaseError:
        logger.exception(f'DB error in command_add_city for user {user_id}')
        await message.answer('Проблема с базой данных, пожалуйста, попробуйте ещё раз или немного позже')

@favourites_router.message(Command('my_cities'))
async def process_command_my_cities(message: Message):
    user_id = message.from_user.id
    
    try:
        await ensure_user(user_id, message.from_user.username)
        cities = await get_user_cities(user_id)
    except DatabaseError:
        logger.exception(f'DB error in my_cities for user {user_id}')
        await message.answer('Проблемы с базой данных, попробуйте позже')
        return

    if not cities:
        await message.answer('У вас пока нет городов в списке избранных')
        return

    cities_list = '\n'.join(cities)
    text = f'Ваши избранные города:\n{cities_list}'

    keyboard = create_cities_keyboard(cities)

    await message.answer(text, reply_markup=keyboard)

@favourites_router.message(Command('remove_city'))
async def process_command_remove_city(message: Message):
    args = message.text.split(maxsplit=1)
    user_id = message.from_user.id

    if len(args) < 2:
        await message.answer('❌ Использование: /remove_city (название_города)\nПример: /remove_city Москва')
        return

    city = clean_city_name(args[1])

    try:
        await ensure_user(user_id, message.from_user.username)
        if await remove_city(user_id, city):
            await message.answer(f'Город: {city} успешно удален из списка избранных')
        else:
            await message.answer(f'Город: {city} не найден в вашем списке!')
    except DatabaseError:
        logger.exception(f'DB error in command_remove_city for user {user_id}')
        await message.answer('Проблема с базой данных, пожалуйста, попробуйте ещё раз или немного позже')
        return

@favourites_router.callback_query(F.data.startswith('city:'))
async def process_city_selection(callback: CallbackQuery):
    action, city = callback.data.split(':', 1)

    keyboard = create_action_keyboard(city)

    await callback.answer()
    await callback.message.edit_text(
        f'Вы выбрали город: <b>{city}</b>\n Что хотите сделать?',
        reply_markup=keyboard
    )

@favourites_router.callback_query(F.data.startswith('weather:'))
async def process_show_weather(callback: CallbackQuery):
    action, city = callback.data.split(':', 1)

    await callback.answer()
    await callback.message.edit_text(
        f'Загружую погоду для города <b>{city}</b>'
    )

    await send_weather_report(callback, city)


@favourites_router.callback_query(F.data.startswith('remove:'))
async def process_remove_city(callback: CallbackQuery):
    action, city = callback.data.split(':', 1)
    user_id = callback.from_user.id
    
    try:
        await ensure_user(user_id, callback.from_user.username)
        await remove_city(user_id, city)

        cities = await get_user_cities(user_id)
    except DatabaseError:
        logger.exception(f'DB error in callback_remove_city for user {user_id}')
        await callback.answer('Проблема с базой данных, пожалуйста, попробуйте ещё раз или немного позже', show_alert=True)
        return

    await callback.answer(f'Город {city} удален')
    if cities:
        keyboard = create_cities_keyboard(cities)
        await callback.message.edit_text(
            f'Город {city} удален.\n\nВаши избранные города',
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text('Город удален. Список избранного пуст')
    

@favourites_router.callback_query(F.data == 'back_to_cities')
async def process_back_to_cities(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    try:
        await ensure_user(user_id, callback.from_user.username)
        cities = await get_user_cities(user_id)
    except DatabaseError:
        logger.exception(f'DB error in back_to_cities for user {user_id}')
        await callback.answer('Проблема с базой данных, пожалуйста, попробуйте ещё раз или немного позже', show_alert=True)
        return

    await callback.answer()
    if cities:
        keyboard = create_cities_keyboard(cities)
        await callback.message.edit_text(
            f'Ваши избранные города', reply_markup=keyboard
        )
    else:
        await callback.message.edit_text('Список избранного пуст')
