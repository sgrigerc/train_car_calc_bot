from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command


base_router = Router()


@base_router.message(CommandStart())
async def start_cmd(message: types.Message):
   chat_id = message.chat.id
   await message.answer('Привет, я умный калькулятор вагонов!')


@base_router.message(Command('lets_go'))
async def echo(message: types.Message):
   await message.answer('Вот дальнейшие действия')
