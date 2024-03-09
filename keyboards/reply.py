# from aiogram.types import KeyboardButton
# from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# from handlers.the_developed_solution import calculate_handler


# async def buttons_with_values(user_id, session, chat_id):
#    values = await calculate_handler(user_id, session)
   
#    keyboard = ReplyKeyboardBuilder
   
#    for index, value in enumerate(values):
#       button = InlineKeyboardBuilder(text=f"Button {index + 1}: {value}", callback_data=f"value_{index + 1}")
#       keyboard.add(button)
