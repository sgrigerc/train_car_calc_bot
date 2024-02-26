from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def user_kb(
   *btns: str,
   placeholder: str = None,
   request_contact: int = None,
   request_location: int = None,
   sizes: tuple[int] = (2,),
):
   keyboard = ReplyKeyboardBuilder()

   for index, text in enumerate(btns, start=0):
      
      if request_contact and request_contact == index:
         keyboard.add(KeyboardButton(text=text, request_contact=True))

      elif request_location and request_location == index:
         keyboard.add(KeyboardButton(text=text, request_location=True))
      else:

         keyboard.add(KeyboardButton(text=text))

   return keyboard.adjust(*sizes).as_markup(
         esize_keyboard=True, input_field_placeholder=placeholder)
