from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Terminals
from sqlalchemy.orm import sessionmaker
from database.engine import engine

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


#хранение нажатых кнопок
user_buttons = {}


async def processing_terminals_button(user_id: int, session: AsyncSession):
   async with SessionLocal() as session:
      user_data = await session.execute(select(Terminals).where(Terminals.user_id == user_id).limit(1))
      user_data = user_data.fetchone()
      
      if user_data:
         for terminal_name in ['Beliy_Rast', 'Elektrougli', 'Vorsino', 'Selyatino', 'Khovrino', 'Ramenskoye', 'Lyubertsy']:
            # if terminal_name in user_buttons.get(user_id, []):
            setattr(user_data, terminal_name, 1 if terminal_name in user_buttons.get(user_id, set()) else 0)
         
      else:
         user_data = Terminals(user_id = user_id)
         for terminal_name in ['Beliy_Rast', 'Elektrougli', 'Vorsino', 'Selyatino', 'Khovrino', 'Ramenskoye', 'Lyubertsy']:
            # if terminal_name in user_buttons.get(user_id, []):
            setattr(user_data, terminal_name, 1 if terminal_name in user_buttons.get(user_id, set()) else 0)
         session.add(user_data)
         
      await session.commit()
      await session.close()
         
      user_buttons.pop(user_id, None)

