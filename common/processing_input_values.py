import cvs

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from database.models import InitialValues, ResultValues
from decimal import Decimal


rate_values = {}

async def calculation_of_intermediate_values(user_id: int, session: AsyncSession):
   result = await session.execute(select(InitialValues).where(InitialValues.user_id == user_id))
   row = result.scalar_one_or_none()
   
   print(row)
   
   if not row:
      raise ValueError(f"Не найдено данных для пользователя {user_id}")
   
   year_of_indexing = float(row.year_of_indexing)
   empty_mileage_distance = float(row.empty_mileage_distance)
   the_number_of_days_of_downtime_at_the_station = float(row.the_number_of_days_of_downtime_at_the_station)
   
   # Определяем indexing
   if year_of_indexing == 2023.0:
      indexing = 5.768
   elif year_of_indexing == 2024.0:
      indexing = 6.2064
   elif year_of_indexing == 2025.0:
      indexing = 6.5291
   
   empty_mileage_ranges = {
      (1, 5): 2.0,
      (6, 10): 9.0,
      (11, 15): 14.0,
      (16, 20): 20.0,
      (21, 25): 25.0,
   }
   
   empty_mileage_rate = next(
      (rate for (lower, upper), rate in empty_mileage_ranges.items() if lower <= empty_mileage_distance < upper),
      0  # значение по умолчанию, если ни один диапазон не соответствует
   )
   
   the_matrix_of_the_rate_values_outside_the_transportation_process_per_POP = {
      1.0: {'at_transfer_stations_less_than_19': 117.86, 'at_transfer_stations_from_19_to_25': 194.63, 'at_transfer_stations_from_25': 225.97, 'at_unloading_stations_less_than_19': 117.86, 'at_unloading_stations_from_19_to_25': 194.63, 'at_unloading_stations_from_25': 225.97},
      2.0: {'at_transfer_stations_less_than_19': 235.72, 'at_transfer_stations_from_19_to_25': 389.36, 'at_transfer_stations_from_25': 451.94, 'at_unloading_stations_less_than_19': 235.72, 'at_unloading_stations_from_19_to_25': 389.26, 'at_unloading_stations_from_25': 451.94},
      3.0: {'at_transfer_stations_less_than_19': 353.58, 'at_transfer_stations_from_19_to_25': 583.89, 'at_transfer_stations_from_25': 677.91, 'at_unloading_stations_less_than_19': 353.58, 'at_unloading_stations_from_19_to_25': 583.89, 'at_unloading_stations_from_25': 677.91},
   }
   
   the_rate_outside_the_transportation_process_per_POP = the_matrix_of_the_rate_values_outside_the_transportation_process_per_POP.get(the_number_of_days_of_downtime_at_the_station, {'at_transfer_stations_less_than_19': 117.86, 'at_transfer_stations_from_19_to_25': 194.63, 'at_transfer_stations_from_25': 225.97, 'at_unloading_stations_less_than 19': 117.86, 'at_unloading_stations_from_19_to_25': 194.63, 'at_unloading_stations_from_25': 225.97})
   
   
   the_cost_of_an_empty_tariff = indexing * empty_mileage_rate #стоимость порожнего тарифа(стоимость подсыла вагона)
   tariff_indexing = indexing   #индескация тарифа
   the_rate_for_an_empty_flight_without_indexing = empty_mileage_rate   #ставка за порожний рейс без индексации
   
   x = the_number_of_days_of_downtime_at_the_station * tariff_indexing  #промежуточное0 чтобы 100 раз не считать
   
   #считаем информацаию о разработанном плане 11 строка ексель
   #ставка за простой на ПОП вне перевозочного процесса на станции выгрузки 
   trfdottpatusalt_19_1 = x * the_rate_outside_the_transportation_process_per_POP['at_transfer_stations_less_than_19']
   trfdottpatusalt_19_25_1 = x * the_rate_outside_the_transportation_process_per_POP['at_transfer_stations_from_19_to_25']
   trfdottpatusalt_25_1 = x * the_rate_outside_the_transportation_process_per_POP['at_transfer_stations_from_25']
   trfdottpatusalt_19_2 = x * the_rate_outside_the_transportation_process_per_POP['at_unloading_stations_less_than_19']
   trfdottpatusalt_19_25_2 = x * the_rate_outside_the_transportation_process_per_POP['at_unloading_stations_from_19_to_25']
   trfdottpatusalt_25_2 = x * the_rate_outside_the_transportation_process_per_POP['at_unloading_stations_from_25']

   #12 строка ексель
   #ставка за простой на поп вне перевозочного процесса на сети жд (+стоимость порожнего тарифа) 
   trfdottpatus_19_1 = ...
   
   

   #the_rate_for_downtime_outside_the_transportation_process_of_the_railway_network = ...
   #the_rate_for_downtime_at_the_pnop_at_the_unloading_station = ...
   #the_rate_for_idle_time_on_the_pnop_in_the_sludge_on_the_railway_network = ...
   
   # Сохраняем результаты в новую таблицу
   result_values_instance = ResultValues(
      user_id = user_id,
      trfdottpatusalt_19_1 = trfdottpatusalt_19_1,
      trfdottpatusalt_19_25_1 = trfdottpatusalt_19_25_1,
      trfdottpatusalt_25_1 = trfdottpatusalt_25_1,
      trfdottpatusalt_19_2 = trfdottpatusalt_19_2,
      trfdottpatusalt_19_25_2 = trfdottpatusalt_19_25_2,
      trfdottpatusalt_25_2 = trfdottpatusalt_25_2
      )
   print(f"Before commit: {ResultValues.__dict__}")
   session.add(result_values_instance)
   await session.commit()
   
   return (
            trfdottpatusalt_19_1,
            trfdottpatusalt_19_25_1,
            trfdottpatusalt_25_1,
            trfdottpatusalt_19_2,
            trfdottpatusalt_19_25_2,
            trfdottpatusalt_25_2
            )