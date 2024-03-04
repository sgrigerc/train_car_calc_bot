'''
здесь будет хендлер котый выдает результат, по инлайн кнопке которая будет выскакивать
после введения последнего значения под сообщением "данные получены!"
кнопка получить результат

и хендлер процесса доходности тоже потом снизу будет выскакивать кнопка сравнить(инлайн)

'''

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker


from common.processing_input_values import calculation_of_intermediate_values
from database.models import InitialValues
from database.engine import engine, session_maker
from decimal import Decimal


SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

getting_values_router = Router()

@getting_values_router.message(Command("calculate"))
async def calculate_handler(message: types.Message, state: FSMContext):
   user_id = message.from_user.id

   # Получаем данные из базы данных
   async with SessionLocal() as session:
      result = await session.execute(select(InitialValues).where(InitialValues.user_id == user_id).order_by(InitialValues.created.desc()).limit(1))      
      row = result.fetchone()

      if not row:
         await message.answer("У вас нет сохраненных данных для расчета.")
         return
      try:
         # Выполняем расчеты
         result = await calculation_of_intermediate_values(user_id, session)  # row, session Передаем row и session в ваш метод calculation_of_intermediate_values
         await message.answer(f"Результат расчетов: {result}")
         row = 0
         
      except Exception as e:
         await message.answer(f"Произошла ошибка при расчетах: {str(e)}")
         print(e)
      
      finally:
         await session.close()
      