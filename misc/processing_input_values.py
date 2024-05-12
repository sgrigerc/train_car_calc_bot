from typing import Dict
import csv
import tracemalloc

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import InitialValues, ResultValues

tracemalloc.start()

async def calculation_of_intermediate_values(user_id: int, session: AsyncSession) -> Dict[str, float]:
   result = await session.execute(select(InitialValues).where(InitialValues.user_id == user_id))
   row = result.scalar_one_or_none()
      
   if not row:
      raise ValueError(f"Не найдено данных для пользователя {user_id}")
   
   year_of_indexing = float(row.year_of_indexing)
   empty_mileage_distance = float(row.empty_mileage_distance)
   the_number_of_days_of_downtime_at_the_station = float(row.the_number_of_days_of_downtime_at_the_station)
   travel_time_to_the_station_on_the_railway_network = float(row.travel_time_to_the_station_on_the_railway_network)
   the_cost_of_the_car = float(row.the_cost_of_the_car)
   the_cost_of_downtime_on_pnop = float(row.the_cost_of_downtime_on_pnop)
   travel_time_to_the_terminal = float(row.travel_time_to_the_terminal)
   
   # Определяем indexing
   indexing_values = {2023.0: 5.768, 2024.0: 6.2064, 2025.0: 6.5291}
   indexing = indexing_values.get(year_of_indexing, 0)
   
   # получаем значение 'ставка за порожний рейс'
   csv_file_empty_mileage_rate = 'misc/csv_files/matrix_the_rate_for_an_empty_flight.csv'
   empty_mileage_rate = await get_empty_mileage_rate(csv_file_empty_mileage_rate, empty_mileage_distance)
   
   the_cost_of_an_empty_tariff = indexing * empty_mileage_rate #стоимость порожнего тарифа(стоимость подсыла вагона)
   tariff_indexing = indexing   #индескация тарифа
   
   csv_file_the_matrix = 'misc/csv_files/values_matrix.csv'
   the_rate_outside_the_transportation_process_per_POP = await getting_the_board_values(csv_file_the_matrix, the_number_of_days_of_downtime_at_the_station)
   
   if the_rate_outside_the_transportation_process_per_POP:
   
      # cчитаем информацаию о разработанном плане 11 строка ексель
      # ставка за простой на ПОП вне перевозочного процесса на станции выгрузки
      x = the_number_of_days_of_downtime_at_the_station * tariff_indexing  # промежуточное, чтобы 100 раз не считать
      
      the_rate_is_beyond_the_stop_on_unloading_19_1 =  round(x * the_rate_outside_the_transportation_process_per_POP['at_transfer_stations_less_than_19'], 2)
      the_rate_is_beyond_the_stop_on_unloading_19_25_1 =  round(x * the_rate_outside_the_transportation_process_per_POP['at_transfer_stations_from_19_to_25'], 2)
      the_rate_is_beyond_the_stop_on_unloading_25_1 =  round(x * the_rate_outside_the_transportation_process_per_POP['at_transfer_stations_from_25'], 2)
      the_rate_is_beyond_the_stop_on_unloading_19_2 =  round(x * the_rate_outside_the_transportation_process_per_POP['at_unloading_stations_less_than_19'], 2)
      the_rate_is_beyond_the_stop_on_unloading_19_25_2 =  round(x * the_rate_outside_the_transportation_process_per_POP['at_unloading_stations_from_19_to_25'], 2)
      the_rate_is_beyond_the_stop_on_unloading_25_2 =  round(x * the_rate_outside_the_transportation_process_per_POP['at_unloading_stations_from_25'], 2)
      
      # 12 строка ексель
      # ставка за простой на поп вне перевозочного процесса на сети жд (+стоимость порожнего тарифа)
      y = travel_time_to_the_station_on_the_railway_network * the_cost_of_the_car + the_number_of_days_of_downtime_at_the_station * tariff_indexing
      
      
      the_rate_on_the_railway_tracks_19_1 = round(y * the_rate_outside_the_transportation_process_per_POP['at_transfer_stations_less_than_19'] + the_cost_of_an_empty_tariff, 2)
      the_rate_on_the_railway_tracks_19_25_1 = round(y * the_rate_outside_the_transportation_process_per_POP['at_transfer_stations_from_19_to_25'], 2)
      the_rate_on_the_railway_tracks_25_1 = round(y * the_rate_outside_the_transportation_process_per_POP['at_transfer_stations_from_25'], 2)
      the_rate_on_the_railway_tracks_19_2 = round(y * the_rate_outside_the_transportation_process_per_POP['at_unloading_stations_less_than_19'], 2)
      the_rate_on_the_railway_tracks_19_25_2 = round(y * the_rate_outside_the_transportation_process_per_POP['at_unloading_stations_from_19_to_25'], 2)
      the_rate_on_the_railway_tracks_25_2 = round(y * the_rate_outside_the_transportation_process_per_POP['at_unloading_stations_from_25'], 2)
      
      
   else:
      print(f"Данные для {the_number_of_days_of_downtime_at_the_station} не найдены.")
      return None
   
   the_rate_for_downtime_at_the_pnop_at_the_unloading_station = round(the_number_of_days_of_downtime_at_the_station * (the_cost_of_downtime_on_pnop + the_cost_of_the_car), 2)
   idle_time_on_the_pnop_in_the_sludge_on_the_railway_network = round(the_number_of_days_of_downtime_at_the_station * (the_cost_of_downtime_on_pnop + the_cost_of_the_car) + the_cost_of_an_empty_tariff + the_cost_of_the_car * travel_time_to_the_terminal, 2)
   
   # Сохраняем результаты в новую таблицу
   result_values_instance = ResultValues(
      user_id = user_id,
      the_rate_is_beyond_the_stop_on_unloading_19_1 = the_rate_is_beyond_the_stop_on_unloading_19_1,
      the_rate_is_beyond_the_stop_on_unloading_19_25_1 = the_rate_is_beyond_the_stop_on_unloading_19_25_1,
      the_rate_is_beyond_the_stop_on_unloading_25_1 = the_rate_is_beyond_the_stop_on_unloading_25_1,
      the_rate_is_beyond_the_stop_on_unloading_19_2 = the_rate_is_beyond_the_stop_on_unloading_19_2,
      the_rate_is_beyond_the_stop_on_unloading_19_25_2 = the_rate_is_beyond_the_stop_on_unloading_19_25_2,
      the_rate_is_beyond_the_stop_on_unloading_25_2 = the_rate_is_beyond_the_stop_on_unloading_25_2,
      the_rate_on_the_railway_tracks_19_1 = the_rate_on_the_railway_tracks_19_1,
      the_rate_on_the_railway_tracks_19_25_1 = the_rate_on_the_railway_tracks_19_25_1,
      the_rate_on_the_railway_tracks_25_1 = the_rate_on_the_railway_tracks_25_1,
      the_rate_on_the_railway_tracks_19_2 = the_rate_on_the_railway_tracks_19_2,
      the_rate_on_the_railway_tracks_19_25_2 = the_rate_on_the_railway_tracks_19_25_2,
      the_rate_on_the_railway_tracks_25_2 = the_rate_on_the_railway_tracks_25_2,
      the_rate_for_downtime_at_the_pnop_at_the_unloading_station = the_rate_for_downtime_at_the_pnop_at_the_unloading_station,
      idle_time_on_the_pnop_in_the_sludge_on_the_railway_network = idle_time_on_the_pnop_in_the_sludge_on_the_railway_network,
      )
   
   session.add(result_values_instance)
   await session.commit()
   
   return {
            'the_rate_is_beyond_the_stop_on_unloading_19_1' : the_rate_is_beyond_the_stop_on_unloading_19_1,
            'the_rate_is_beyond_the_stop_on_unloading_19_25_1' : the_rate_is_beyond_the_stop_on_unloading_19_25_1,
            'the_rate_is_beyond_the_stop_on_unloading_25_1' : the_rate_is_beyond_the_stop_on_unloading_25_1,
            'the_rate_is_beyond_the_stop_on_unloading_19_2' : the_rate_is_beyond_the_stop_on_unloading_19_2,
            'the_rate_is_beyond_the_stop_on_unloading_19_25_2' : the_rate_is_beyond_the_stop_on_unloading_19_25_2,
            'the_rate_is_beyond_the_stop_on_unloading_25_2' : the_rate_is_beyond_the_stop_on_unloading_25_2,
            'the_rate_on_the_railway_tracks_19_1' : the_rate_on_the_railway_tracks_19_1,
            'the_rate_on_the_railway_tracks_19_25_1' : the_rate_on_the_railway_tracks_19_25_1,
            'the_rate_on_the_railway_tracks_25_1' : the_rate_on_the_railway_tracks_25_1,
            'the_rate_on_the_railway_tracks_19_2' : the_rate_on_the_railway_tracks_19_2,
            'the_rate_on_the_railway_tracks_19_25_2' : the_rate_on_the_railway_tracks_19_25_2,
            'the_rate_on_the_railway_tracks_25_2' : the_rate_on_the_railway_tracks_25_2,
            'the_rate_for_downtime_at_the_pnop_at_the_unloading_station' : the_rate_for_downtime_at_the_pnop_at_the_unloading_station,
            'idle_time_on_the_pnop_in_the_sludge_on_the_railway_network' : idle_time_on_the_pnop_in_the_sludge_on_the_railway_network,
            }


async def getting_the_board_values(csv_file: str, the_number_of_days_of_downtime_at_the_station: float):
   with open(csv_file, newline='') as csvfile:
      reader = csv.DictReader(csvfile, delimiter=';')
      for row in reader:
         
         #провера значения
         if the_number_of_days_of_downtime_at_the_station > 60:
            return {
               'at_transfer_stations_less_than_19': 1000.10,
               'at_transfer_stations_from_19_to_25': 1100.95,
               'at_transfer_stations_from_25': 1200.0,
               'at_unloading_stations_less_than_19': 1000.10,
               'at_unloading_stations_from_19_to_25': 1100.95,
               'at_unloading_stations_from_25': 1200.0,  
            }
         
         if float(row['the_number_of_days_of_downtime_at_the_station']) == the_number_of_days_of_downtime_at_the_station:
            return{
               'at_transfer_stations_less_than_19': float(row['at_transfer_stations_less_than_19']),
               'at_transfer_stations_from_19_to_25': float(row['at_transfer_stations_from_19_to_25']),
               'at_transfer_stations_from_25': float(row['at_transfer_stations_from_25']),
               'at_unloading_stations_less_than_19': float(row['at_unloading_stations_less_than_19']),
               'at_unloading_stations_from_19_to_25': float(row['at_unloading_stations_from_19_to_25']),
               'at_unloading_stations_from_25': float(row['at_unloading_stations_from_25']),
            }
   return None


async def get_empty_mileage_rate(csv_file: str, empty_mileage_distance: float):
   with open(csv_file, newline='') as csvfile:
      reader = csv.DictReader(csvfile, delimiter=';')
      for row in reader:
         beginning, end, tariff_scheme = map(float, [row['beginning'], row['end'], row['tariff_scheme']])
         
         if beginning <= empty_mileage_distance <= end:
            return tariff_scheme
   return 0


async def get_value_from_database(user_id: int, value_name: str, session: AsyncSession) -> float:
   try:
      result = await session.execute(
         select(getattr(ResultValues, value_name)).where(ResultValues.user_id == user_id)
      )
      return result.scalar_one_or_none()
   except Exception as e:
      print(f"Ошибка при получении значений: {str(e)}")
      return None


async def translate_names(values):
   translations = {
      'the_rate_is_beyond_the_stop_on_unloading_19_1' : 'ставка за простой на поп вне перевозочного процесса на станциях перемещения при: менее 19.6 м.',
      'the_rate_is_beyond_the_stop_on_unloading_19_25_1' : 'ставка за простой на поп вне перевозочного процесса на станциях перемещения при: от 19.6 до 25.5 м.',
      'the_rate_is_beyond_the_stop_on_unloading_25_1' : 'ставка за простой на поп вне перевозочного процесса на станциях перемещения при: 25.5 м. и более',
      'the_rate_is_beyond_the_stop_on_unloading_19_2' : 'ставка за простой на поп вне перевозочного процесса на станциях выгрузки при: менее 19.6 м.',
      'the_rate_is_beyond_the_stop_on_unloading_19_25_2' : 'ставка за простой на поп вне перевозочного процесса на станциях выгрузки при: от 19.6 до 25.5 м.',
      'the_rate_is_beyond_the_stop_on_unloading_25_2' : 'ставка за простой на поп вне перевозочного процесса на станциях выгрузки при: 25.5 м. и более',
      'the_rate_on_the_railway_tracks_19_1' : 'ставка за простой на поп вне перевозочного процесса на сети жд (+стоимость порожнего тарифа) при: менее 19.6 м.',
      'the_rate_on_the_railway_tracks_19_25_1' : 'ставка за простой на поп вне перевозочного процесса на сети жд (+стоимость порожнего тарифа) при: от 19.6 до 25.5 м.',
      'the_rate_on_the_railway_tracks_25_1' : 'ставка за простой на поп вне перевозочного процесса на сети жд (+стоимость порожнего тарифа) при: 25.5 м. и более',
      'the_rate_on_the_railway_tracks_19_2' : 'ставка за простой на поп вне перевозочного процесса на сети жд (+стоимость порожнего тарифа) при: менее 19.6 м.(2??)',
      'the_rate_on_the_railway_tracks_19_25_2' : 'ставка за простой на поп вне перевозочного процесса на сети жд (+стоимость порожнего тарифа) при: от 19.6 до 25.5 м.(2??)',
      'the_rate_on_the_railway_tracks_25_2' : 'ставка за простой на поп вне перевозочного процесса на сети жд (+стоимость порожнего тарифа) при: 25.5 м. и более(2??)',
      'the_rate_for_downtime_at_the_pnop_at_the_unloading_station' : 'ставка за простой на пноп на станции выгрузки',
      'idle_time_on_the_pnop_in_the_sludge_on_the_railway_network' : 'ставка за простой на пноп в отстое на сети жд',
   }

   #переводим в нормальный язык
   translated_names = [translations.get(value['name'], value['name']) for value in values]

   return translated_names


async def margin_calculation_func(values, sate):
   marginality_percentage = 0.15
   values_float = [{'name': value['name'], 'value': float(value['value'])} for value in values]
   marginality = [round(value['value'] * (1 + marginality_percentage), 2) for value in values_float]
   margin = [round(marginality_value - float(value['value']), 2) for value, marginality_value in zip(values_float, marginality)]
   
   return margin


async def calculate_margin_with_translations(values, state):
   translated_names = await translate_names(values)
   result = await margin_calculation_func(values, state)

   # Собираем строки с названием и рассчитанными значениями
   result_str = "\n".join([f'{i + 1}. {name}: {margin}' for i, (name, margin) in enumerate(zip(translated_names, result))])

   return result_str


