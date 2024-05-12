from aiogram.fsm.context import FSMContext
from aiogram import types

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Terminals
from sqlalchemy.orm import sessionmaker
from database.engine import engine
from datetime import datetime
from typing import List

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

#хранение нажатых кнопок
user_buttons = {}
terminal_buttons = {
         'Белый Раст': 'Beliy_Rast', 
         'Электроугли': 'Elektrougli', 
         'Ворсино': 'Vorsino',
         'Селятино': 'Selyatino',
         'Ховрино': 'Khovrino',
         'Раменское': 'Ramenskoye',
         'Люберцы': 'Lyubertsy',
         # 'Далее': 'next'
      }
all_terminals = {'Beliy_Rast', 'Elektrougli', 'Vorsino', 'Selyatino', 'Khovrino', 'Ramenskoye', 'Lyubertsy'}


async def processing_terminals_button(user_id: int, session: AsyncSession):
   async with SessionLocal() as session:
      chosen_terminals = user_buttons.get(user_id, set())
      missing_terminals = all_terminals - chosen_terminals
      user_buttons[user_id] = missing_terminals
      
      user_data = await session.execute(select(Terminals).where(Terminals.user_id == user_id).limit(1))
      user_data = user_data.fetchone()
      
      if user_data:
         for terminal_name in all_terminals:
            setattr(user_data, terminal_name, 1 if terminal_name in user_buttons.get(user_id, set()) else 0)
         
      else:
         user_data = Terminals(user_id = user_id)
         for terminal_name in all_terminals:
            setattr(user_data, terminal_name, 1 if terminal_name in user_buttons.get(user_id, set()) else 0)
         session.add(user_data)
         
      await session.commit()
      await session.close()
      
      user_buttons.pop(user_id, None)


async def get_selected_terminals(user_id: int, session: AsyncSession) -> List[str]:
      selected_terminals = []
      user_data = await session.execute(select(Terminals).where(Terminals.user_id == user_id).limit(1))
      user_data = user_data.fetchone()
      
      if user_data:
         for terminal_column in ['Beliy_Rast', 'Elektrougli', 'Vorsino', 'Selyatino', 'Khovrino', 'Ramenskoye', 'Lyubertsy']:
            if hasattr(user_data,terminal_column) and getattr(user_data, terminal_column) == 1:
               selected_terminals.append(terminal_column)
      return selected_terminals


# вычисляем количество дней (Дельта между датой погрузки ПС и плановой даты погрузки)
async def calculate_date_delta(date_of_readiness: str, loading_date: str) -> int:
   date_format = "%d.%m"
   
   try:
      date_of_readiness = datetime.strptime(date_of_readiness, date_format)
      loading_date = datetime.strptime(loading_date, date_format)
      
      delta = loading_date - date_of_readiness
      print(delta.days)
      return delta.days
   except ValueError:
      print("Неправильный формат даты")
      return None 
