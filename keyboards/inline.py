from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from common.processing_input_values import calculation_of_intermediate_values

def get_callback_btns(
    *,
   btns: dict[str, str],
   sizes: tuple[int] = (1,)):

   keyboard = InlineKeyboardBuilder()

   for text, data in btns.items():
      keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

   return keyboard.adjust(*sizes).as_markup()


async def buttons_with_values(user_id, session):
   values = await calculation_of_intermediate_values(user_id, session)
   keyboard = InlineKeyboardBuilder()
   
   for index, value in enumerate(values):
      keyboard.add(InlineKeyboardButton(text=str(value), callback_data=f"value_{index + 1}"))
      
   return keyboard.adjust(1).as_markup()

