from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from misc.processing_input_values import get_value_from_database, calculate_margin_with_translations

from keyboards.inline import buttons_with_values
from database.models import InitialValues
from database.engine import engine


SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
getting_values_router = Router()


# 
@getting_values_router.callback_query(F.data.startswith('calculate'))
async def calculate_handler(callback: types.CallbackQuery):
   user_id = callback.from_user.id
   # Получаем данные из бд
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


# получаем значения от пользователя
@getting_values_router.callback_query(F.data.startswith('value_'))
async def margin_calculation(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
   user_id = callback.from_user.id
   value_name = callback.data.split('value_')[-1]
   data = await state.get_data()
   values = data.get('values', [])

   # Получаем значение из бд по названию
   value = await get_value_from_database(user_id, value_name, session)

   if value is not None:
      values.append({'name': value_name, 'value': value})
      await state.update_data(values=values)
      await callback.answer(f'Значение: {value_name} - {value}')
   else:
      await callback.answer(f'Значение {value_name} не найдено в базе данных.')


# обрабатываем значения
@getting_values_router.callback_query(F.data.startswith('calc_margin'))
async def calculate_the_margin(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
   data = await state.get_data()
   
   if 'values' in data:
      values = data['values']
      result_str = await calculate_margin_with_translations(values, state)

      # Отправка результата пользователю
      await callback.message.answer(f'Маржа:\n{result_str}')
      await state.clear()
   else:
      await callback.answer(f'Нет выбранных значений для расчета маржи.')
