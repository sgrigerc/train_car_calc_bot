# import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import dotenv_values, find_dotenv, load_dotenv
from aiogram.fsm.strategy import FSMStrategy

load_dotenv(find_dotenv())

# #Получение токена из файла .env
# # config = dotenv_values('./config/.env')
# API_TOKEN = config['API_TOKEN']
# # ADMIN = int(config['ADMIN'])

# #Настройка логов
# logging.basicConfig(level=logging.INFO)

# #Запуск бота и диспетчера
bot = Bot(token=os.getenv('API_TOKEN'))
dp = Dispatcher(fsm_strategy= FSMStrategy.USER_IN_CHAT)






