from sqlalchemy import DateTime , Float, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
   created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class InitialValues(Base):
   __tablename__ = 'i_values'
   
   id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
   the_number_of_days_of_downtime_at_the_station:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   idle_time_at_the_terminal_before_loading:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_cost_of_downtime_on_pnop:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_cost_of_the_car:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   travel_time_to_the_station_on_the_railway_network:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   throwing_time_on_request:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   empty_mileage_distance:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   year_of_indexing:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   travel_time_to_the_terminal:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   
   def __init__(
      self,
      the_number_of_days_of_downtime_at_the_station,
      idle_time_at_the_terminal_before_loading,
      the_cost_of_downtime_on_pnop,
      the_cost_of_the_car,
      travel_time_to_the_station_on_the_railway_network,
      throwing_time_on_request,
      empty_mileage_distance,
      year_of_indexing,
      travel_time_to_the_terminal,
   ):
      self.the_number_of_days_of_downtime_at_the_station = the_number_of_days_of_downtime_at_the_station
      self.idle_time_at_the_terminal_before_loading = idle_time_at_the_terminal_before_loading
      self.the_cost_of_downtime_on_pnop = the_cost_of_downtime_on_pnop
      self.the_cost_of_the_car = the_cost_of_the_car
      self.travel_time_to_the_station_on_the_railway_network = travel_time_to_the_station_on_the_railway_network
      self.throwing_time_on_request = throwing_time_on_request
      self.empty_mileage_distance = empty_mileage_distance
      self.year_of_indexing = year_of_indexing
      self.travel_time_to_the_terminal = travel_time_to_the_terminal
   
   