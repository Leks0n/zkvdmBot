from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

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
async def process_echo_message(message: Message):
    await message.answer(
        f'Ты написал: {message.text} \n'
        'Скоро я буду показывать погоду в этом городе'
    )
