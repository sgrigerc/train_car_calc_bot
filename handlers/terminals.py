from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import engine
from database.orm_query import save_delta_to_database
from keyboards.inline import get_callback_btns
from misc.processing_terminals import (processing_terminals_button,
                                       user_buttons, 
                                       get_selected_terminals, 
                                       calculate_date_delta,
                                       )


terminal_router = Router()
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

all_terminals = {'Beliy_Rast', 'Elektrougli', 'Vorsino', 'Selyatino', 'Khovrino', 'Ramenskoye', 'Lyubertsy'}


class TerminalState(StatesGroup):
   user_id = State()
   selected_terminal = State()   #выьранный терминал
   date_of_readiness_ps = State()   # дата готовности пс
   loading_date = State()  # плановая дата погрузки


# выводим пользователю список терминалов
@terminal_router.message(StateFilter(None), Command('work'))
async def names_of_terminals(message: types.Message):
   await message.answer("Выберите терминал (1 шт.):", reply_markup=await get_callback_btns(btns={
         'Белый Раст': 'Beliy_Rast', 
         'Электроугли': 'Elektrougli', 
         'Ворсино': 'Vorsino',
         'Селятино': 'Selyatino',
         'Ховрино': 'Khovrino',
         'Раменское': 'Ramenskoye',
         'Люберцы': 'Lyubertsy',
         # 'Далее': 'next'
      })) 


# принимаем от пользователя терминалы (обработка нажимаемых кнопок)
@terminal_router.callback_query(StateFilter(None), F.data.in_(all_terminals))  #F.data.in_(all_terminals)
async def processing_of_select_terminals(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession,):
   async with AsyncSession() as session:
      user_id = callback.from_user.id
      
      # запись в БД terminals выбранный теримнал
      # await processing_terminals_button(user_id, session)
      
      await state.update_data(user_id=user_id)
      await state.update_data(selected_terminal = callback.data)
      await callback.message.answer(f"Дата готовности подвижного состава (день.месяц):")
      await state.set_state(TerminalState.date_of_readiness_ps)


# Принимаем дату готовности ПС
@terminal_router.message(TerminalState.date_of_readiness_ps, F.text)
async def handler_date_of_readiness(message: types.Message, state: FSMContext, session: AsyncSession):
   await state.update_data(date_of_readiness=message.text)
   await message.answer(f"Плановая дата погрузки (день.месяц)")
   await state.set_state(TerminalState.loading_date)


# принимаем планову дату погрузки и рассчитываем дельта
@terminal_router.message(TerminalState.loading_date, F.text)
async def handle_of_loading_dates(message: types.Message, state: FSMContext, session: AsyncSession):
   user_id = message.from_user.id
   loading_date = message.text

   data = await state.get_data()
   selected_terminal = data['selected_terminal']
   date_of_readiness = data['date_of_readiness']
   
   try:
      delta = await calculate_date_delta(date_of_readiness, loading_date)
      data['delta'] = delta
      await save_delta_to_database(session, selected_terminal, delta, data)
      await message.answer("Дельта сохранена!")
   
   except Exception as e:
      await message.answer("Ошибка при расчетах. Пожалуйста попробуйте снова")