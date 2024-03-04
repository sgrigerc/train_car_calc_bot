from sqlalchemy import DateTime , Float, func, BigInteger, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
   created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

   def __init__(self, created=None):
      self.created = created

class InitialValues(Base):
   __tablename__ = 'i_values'
   
   id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
   user_id: Mapped[int] = mapped_column(Integer, nullable=False)
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
      user_id,
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
      self.user_id = user_id
      self.the_number_of_days_of_downtime_at_the_station = the_number_of_days_of_downtime_at_the_station
      self.idle_time_at_the_terminal_before_loading = idle_time_at_the_terminal_before_loading
      self.the_cost_of_downtime_on_pnop = the_cost_of_downtime_on_pnop
      self.the_cost_of_the_car = the_cost_of_the_car
      self.travel_time_to_the_station_on_the_railway_network = travel_time_to_the_station_on_the_railway_network
      self.throwing_time_on_request = throwing_time_on_request
      self.empty_mileage_distance = empty_mileage_distance
      self.year_of_indexing = year_of_indexing
      self.travel_time_to_the_terminal = travel_time_to_the_terminal


class ResultValues(Base):
   __tablename__ = 'r_values'
   
   id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
   user_id: Mapped[int] = mapped_column(Integer, nullable=False)
   trfdottpatusalt_19_1:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   trfdottpatusalt_19_25_1:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   trfdottpatusalt_25_1:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   trfdottpatusalt_19_2:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   trfdottpatusalt_19_25_2:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   trfdottpatusalt_25_2:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_on_the_railway_tracks_19_1:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_on_the_railway_tracks_19_25_1:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_on_the_railway_tracks_25_1:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_on_the_railway_tracks_19_1:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_on_the_railway_tracks_19_25_1:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_on_the_railway_tracks_25_1:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_for_downtime_at_the_pnop_at_the_unloading_station:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_for_idle_time_on_the_pnop_in_the_sludge_on_the_railway_network:Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   
   def __init__(
      self,
      user_id,
      trfdottpatusalt_19_1,
      trfdottpatusalt_19_25_1,
      trfdottpatusalt_25_1,
      trfdottpatusalt_19_2,
      trfdottpatusalt_19_25_2,
      trfdottpatusalt_25_2,
      the_rate_on_the_railway_tracks_19_1,
      the_rate_on_the_railway_tracks_19_25_1,
      the_rate_on_the_railway_tracks_25_1,
      the_rate_on_the_railway_tracks_19_2,
      the_rate_on_the_railway_tracks_19_25_2,
      the_rate_on_the_railway_tracks_25_2,
      the_rate_for_downtime_at_the_pnop_at_the_unloading_station,
      the_rate_for_idle_time_on_the_pnop_in_the_sludge_on_the_railway_network
   ):
      self.user_id = user_id
      self.trfdottpatusalt_19_1 = trfdottpatusalt_19_1
      self.trfdottpatusalt_19_25_1 = trfdottpatusalt_19_25_1
      self.trfdottpatusalt_25_1 = trfdottpatusalt_25_1
      self.trfdottpatusalt_19_2 = trfdottpatusalt_19_2
      self.trfdottpatusalt_19_25_2 = trfdottpatusalt_19_25_2
      self.trfdottpatusalt_25_2 = trfdottpatusalt_25_2
      self.the_rate_on_the_railway_tracks_19_1 = the_rate_on_the_railway_tracks_19_1
      self.the_rate_on_the_railway_tracks_19_25_1 = the_rate_on_the_railway_tracks_19_25_1
      self.the_rate_on_the_railway_tracks_25_1 = the_rate_on_the_railway_tracks_25_1
      self.the_rate_on_the_railway_tracks_19_2 = the_rate_on_the_railway_tracks_19_2
      self.the_rate_on_the_railway_tracks_19_25_2 = the_rate_on_the_railway_tracks_19_25_2
      self.the_rate_on_the_railway_tracks_25_2 = the_rate_on_the_railway_tracks_25_2
      self.the_rate_for_downtime_at_the_pnop_at_the_unloading_station = the_rate_for_downtime_at_the_pnop_at_the_unloading_station
      self.the_rate_for_idle_time_on_the_pnop_in_the_sludge_on_the_railway_network = the_rate_for_idle_time_on_the_pnop_in_the_sludge_on_the_railway_network

