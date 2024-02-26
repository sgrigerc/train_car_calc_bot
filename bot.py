import logging
import sys

import asyncio
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from database.engine import create_db, drop_db, session_maker
from config.bot_config import bot, dp
# from middlewares.db import CounterMiddleware
from handlers.base import base_router
from handlers.car_calculator import calculator_router
from common.bot_comman_list import private
from middlewares.db import DataBaseSession


dp.include_router(base_router)
dp.include_router(calculator_router)

#Ограничение типов апдейтов (входящих сообщений)
ALLOWED_UPDATES = ['message, edited_message']


async def on_startup(bot):
   
   run_param = False
   if run_param:
      await drop_db()
      
   await create_db()


async def on_shutdown(bot):
   print("Бот лег!)) (((")

async def main():
   dp.startup.register(on_startup)
   dp.shutdown.register(on_shutdown)
   
   dp.update.middleware(DataBaseSession(session_pool=session_maker))
   
   await create_db()
   await bot.delete_webhook(drop_pending_updates=True)
   await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
   await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == '__main__':
   logging.basicConfig(level=logging.INFO, stream=sys.stdout)
   try:
      print('бот запущен')
      asyncio.run(main())
   except (KeyboardInterrupt, SystemExit):
      logging.info("Bot stopped!")


