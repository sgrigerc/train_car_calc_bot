from sqlalchemy.ext.asyncio import AsyncSession

from database.models import InitialValues


async def orm_add_values(session: AsyncSession, data: dict):
   obj = InitialValues(
         int(data.get('user_id', 0)),
         float(data['the_number_of_days_of_downtime_at_the_station']),
         float(data['idle_time_at_the_terminal_before_loading']),
         float(data['the_cost_of_downtime_on_pnop']),
         float(data['the_cost_of_the_car']),
         float(data['travel_time_to_the_station_on_the_railway_network']),
         float(data['throwing_time_on_request']),
         float(data['empty_mileage_distance']),
         float(data['year_of_indexing']),
         float(data['travel_time_to_the_terminal']),
      )
   session.add(obj)
   await session.commit()