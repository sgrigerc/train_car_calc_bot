from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import InitialValues
from database.orm_query import orm_add_values

from keyboards.inline import get_callback_btns


calculator_router = Router()

#Машина состояний
class CalculationOfCar(StatesGroup):
   user_id = State()
   the_number_of_days_of_downtime_at_the_station = State()    # количество суток простоя на станции
   idle_time_at_the_terminal_before_loading = State()   #время простоя на терминале до погрузки
   the_cost_of_downtime_on_pnop = State()   #стоимость простоя пноп
   the_cost_of_the_car = State()   #себестоимость вагона
   travel_time_to_the_station_on_the_railway_network = State()   #время хода до станции на сети жд (в днях)
   throwing_time_on_request = State()    #время бросания по заявке (в днях)
   empty_mileage_distance = State()   #расстояние порожнего пробега
   year_of_indexing = State()  #год индексации
   travel_time_to_the_terminal = State()    #время хода до терминала (в днях)


#Машина состояний (FSM)
#количество суток простоя на станции
@calculator_router.message(StateFilter(None), Command('work'))
async def first_value(message: types.Message, state: FSMContext):
   user_id = message.from_user.id
   await message.answer("Введите количество суток простоя на станции:")
   await state.set_state(CalculationOfCar.the_number_of_days_of_downtime_at_the_station)
   await state.update_data(user_id=user_id)


#отмена действий
@calculator_router.message(StateFilter('*'), Command("отмена"))
@calculator_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
   
   current_state = await state.get_state()
   if current_state is None:
      return
   
   await state.clear()
   await message.answer("Действия отменены")


#время простоя на терминале до погрузки
@calculator_router.message(CalculationOfCar.the_number_of_days_of_downtime_at_the_station, F.text)
async def second_value(message: types.Message, state: FSMContext):
   await state.update_data(the_number_of_days_of_downtime_at_the_station=message.text)
   await message.answer("Введите время простоя на терминале до погрузки:")
   await state.set_state(CalculationOfCar.idle_time_at_the_terminal_before_loading)



#стоимость простоя пноп
@calculator_router.message(CalculationOfCar.idle_time_at_the_terminal_before_loading, F.text)
async def third_value(message: types.Message, state: FSMContext):
   await state.update_data(idle_time_at_the_terminal_before_loading=message.text)
   await message.answer("Введите стоимость простоя пноп:")
   await state.set_state(CalculationOfCar.the_cost_of_downtime_on_pnop)


#себестоимость вагона
@calculator_router.message(CalculationOfCar.the_cost_of_downtime_on_pnop, F.text)
async def fourth_value(message: types.Message, state: FSMContext):
   await state.update_data(the_cost_of_downtime_on_pnop=message.text)
   await message.answer("Введите себестоимость вагона:")
   await state.set_state(CalculationOfCar.the_cost_of_the_car)


#время хода до станции на сети жд (в днях)
@calculator_router.message(CalculationOfCar.the_cost_of_the_car, F.text)
async def fifth_value(message: types.Message, state: FSMContext):
   await state.update_data(the_cost_of_the_car=message.text)   
   await message.answer("Введите время хода до станции на сети жд (в днях):")
   await state.set_state(CalculationOfCar.travel_time_to_the_station_on_the_railway_network)


#время бросания по заявке (в днях)
@calculator_router.message(CalculationOfCar.travel_time_to_the_station_on_the_railway_network, F.text)
async def sixth_value(message: types.Message, state: FSMContext):
   await state.update_data(travel_time_to_the_station_on_the_railway_network=message.text)
   await message.answer("Введите время бросания по заявке (в днях):")
   await state.set_state(CalculationOfCar.throwing_time_on_request)


#расстояние порожнего пробега
@calculator_router.message(CalculationOfCar.throwing_time_on_request, F.text)
async def seventh_value(message: types.Message, state: FSMContext):
   await state.update_data(throwing_time_on_request=message.text)
   await message.answer("Введите расстояние порожнего пробега:")
   await state.set_state(CalculationOfCar.empty_mileage_distance)


#год индексации
@calculator_router.message(CalculationOfCar.empty_mileage_distance, F.text)
async def eleventh_value(message: types.Message, state: FSMContext):
   await state.update_data(empty_mileage_distance=message.text)
   await message.answer("Введите год индексации:")
   await state.set_state(CalculationOfCar.year_of_indexing)


#время хода до терминала (в днях)
@calculator_router.message(CalculationOfCar.year_of_indexing, F.text)
async def ninth_value(message: types.Message, state: FSMContext):
   await state.update_data(year_of_indexing=message.text)
   await message.answer("Введите время хода до терминала (в днях):")
   await state.set_state(CalculationOfCar.travel_time_to_the_terminal)


#сохраняем полученные данные ( вылезает кнопка готово)
@calculator_router.message(CalculationOfCar.travel_time_to_the_terminal, F.text)
async def the_end_of_the_calculations(message: types.Message, state: FSMContext, session: AsyncSession):
   await state.update_data(travel_time_to_the_terminal=message.text)
   data = await state.get_data()
   try:
      await orm_add_values(session, data)
      await state.clear()
      await message.answer("Данные получены!", reply_markup=get_callback_btns(btns={'калькулировать': 'calculate'})) 
      
   except Exception as e:
      await message.answer('Что то пошло не так...') 
      await state.clear()


