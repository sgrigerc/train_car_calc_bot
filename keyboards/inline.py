from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder 

from misc.processing_input_values import calculation_of_intermediate_values, translate_names

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

async def get_callback_btns(
   *,
   btns: dict[str, str],
   sizes: tuple[int] = (1,)):

   keyboard = InlineKeyboardBuilder()

   for text, data in btns.items():
      keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

   return keyboard.adjust(*sizes).as_markup()


async def buttons_with_values(user_id, session):
   try:
      values = await calculation_of_intermediate_values(user_id, session)
      keyboard = InlineKeyboardBuilder()

      for value_name, value in values.items():
         keyboard.add(InlineKeyboardButton(text=str(value), callback_data=f"value_{value_name}"))
      keyboard.add(InlineKeyboardButton(text="Далее", callback_data="percent_margin"))
      
      return keyboard.adjust(1).as_markup()
   except Exception as e:
      print(f"Error in buttons_with_values: {str(e)}")
      raise


# async def button_names(user_id, session):
#    try:
#       values = await calculation_of_intermediate_values(user_id, session)
#       keyboard = InlineKeyboardBuilder()
#       button_name = []
      
#       for value_name, value in value.items():
#          translated_name = translate_names(value_name)
#          button_name.append(translated_name)
         
#          keyboard.add(InlineKeyboardButton(text=f"translated_name"): {value}, callback_data=f"value_{value_name}")
      
#    except:
      
# inline_keyboard = InlineKeyboardMarkup(row_width=1)
# next_button = InlineKeyboardButton("Далее", callback_data="next_command")
# inline_keyboard.add(next_button)