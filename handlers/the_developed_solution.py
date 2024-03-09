from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker


from common.processing_input_values import calculation_of_intermediate_values
from keyboards.inline import buttons_with_values
from database.models import InitialValues
from database.engine import engine, session_maker
from decimal import Decimal


SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

getting_values_router = Router()

@getting_values_router.callback_query(F.data.startswith('calculate'))
async def calculate_handler(callback: types.CallbackQuery, state: FSMContext):
   user_id = callback.from_user.id

   # Получаем данные из базы данных
   async with SessionLocal() as session:
      result = await session.execute(select(InitialValues).where(InitialValues.user_id == user_id).order_by(InitialValues.created.desc()).limit(1))      
      row = result.fetchone()

      if not row:
            return await callback.message.answer("У вас нет сохраненных данных для расчета.")
      try:
            await callback.message.answer("Выберите значение:", reply_markup=await buttons_with_values(user_id, session))
      except Exception as e:
            await callback.message.answer(f"Произошла ошибка при расчетах: {str(e)}")
            print(e)
      finally:
            await session.close()



