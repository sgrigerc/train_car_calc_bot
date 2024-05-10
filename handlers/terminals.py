from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import engine
from keyboards.inline import get_callback_btns
from misc.processing_terminals import processing_terminals_button, user_buttons


terminal_router = Router()
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

#хранение нажатых кнопок
# user_buttons = {}

class TerminalState(StatesGroup):
   names_of_terminals = State()  #терминалы
   date_of_readiness_ps = State()   # дата готовности пс
   planned_loading = State()  # плановая дата


# даем пользователю список терминалов
@terminal_router.message(Command('work'))
async def names_of_terminals(message: types.Message, session: AsyncSession):
   await message.answer("Выберите терминал:", reply_markup=await get_callback_btns(btns={
         'Белый Раст': 'Beliy_Rast', 
         'Электроугли': 'Elektrougli', 
         'Ворсино': 'Vorsino',
         'Селятино': 'Selyatino',
         'Ховрино': 'Khovrino',
         'Раменское': 'Ramenskoye',
         'Люберцы': 'Lyubertsy',
         'Далее': 'next'
      })) 


# принимаем от пользователя терминалы (обработка нажимаемых кнопок)
@terminal_router.callback_query(F.data.in_({'Beliy_Rast', 'Elektrougli', 'Vorsino', 'Selyatino', 'Khovrino', 'Ramenskoye', 'Lyubertsy', 'next'}))
async def processing_of_select_terminals(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
   async with AsyncSession() as session:
      button_data = callback.data
      user_id = callback.from_user.id
      
      if button_data != 'next':
         if user_id not in user_buttons:
            user_buttons[user_id] = set()
         user_buttons[user_id].add(button_data)
      else:
         #проверка выбранных терминалов
         all_terminals = {'Beliy_Rast', 'Elektrougli', 'Vorsino', 'Selyatino', 'Khovrino', 'Ramenskoye', 'Lyubertsy', 'next'}
         chosen_terminals = user_buttons.get(user_id, set())
         missing_terminals = all_terminals - chosen_terminals
         user_buttons[user_id] != missing_terminals
         
         await processing_terminals_button(user_id, session)
      
      await callback.answer("Принял терминал")
   
   # terminal_name = callback.data
   # data = await state.get_data()
   # chosen_terminals = data.get('chosen_terminals', [])
   # chosen_terminals.append(terminal_name)
   
   # await state.update_data(chosen_terminals=chosen_terminals)

@terminal_router.message(F.data.in_(['next']))
async def handler_date_of_readiness(callback: types.CallbackQuery, state: FSMContext):
   await callback.message.answer('Дата готовности подвижного состава?')
   await TerminalState.date_of_readiness_ps.set()

# принимаем готовность пс
@terminal_router.message(TerminalState.date_of_readiness_ps)
async def handle_first_number(message: types.Message, state: FSMContext):
   first_number = message.text
   await state.update_data(first_number=first_number)
   await message.answer("Плановая дата погрузки?")
   await TerminalState.planned_loading.set()


# принимаем плановую дату погрузки
@terminal_router.message(TerminalState.planned_loading)
async def handle_second_number(message: types.Message, state: FSMContext):
   second_number = message.text
   await state.update_data(second_number=second_number)
   await message.answer("Данные сохранены. Можете продолжить.")
   await state.finish()



