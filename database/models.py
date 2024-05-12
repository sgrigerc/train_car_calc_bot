from sqlalchemy import DateTime , Float, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
   created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

   def __init__(self, created=None):
      self.created = created


class Delta(Base):
   __tablename__ = 'delta'
   
   user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
   selected_terminal: Mapped[str] = mapped_column(String(40), default=0)
   delta: Mapped[int] = mapped_column(Integer, default=0)
   
   def __init__(
      self, 
      user_id,
      selected_terminal,
      delta,

   ):
      self.user_id = user_id
      self.selected_terminal = selected_terminal
      self.delta = delta


class Terminals(Base):
   __tablename__ = 'terminals'
   
   user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
   Beliy_Rast: Mapped[int] = mapped_column(Integer, default=0)
   Elektrougli: Mapped[int] = mapped_column(Integer, default=0)
   Vorsino: Mapped[int] = mapped_column(Integer, default=0)
   Selyatino: Mapped[int] = mapped_column(Integer, default=0)
   Khovrino: Mapped[int] = mapped_column(Integer, default=0)
   Ramenskoye: Mapped[int] = mapped_column(Integer, default=0)
   Lyubertsy: Mapped[int] = mapped_column(Integer, default=0)
   
   def __init__(
      self, 
      user_id,
      Beliy_Rast=0,
      Elektrougli=0,
      Vorsino=0,
      Selyatino=0,
      Khovrino=0,
      Ramenskoye=0,
      Lyubertsy=0
   ):
      self.user_id = user_id
      self.Beliy_Rast = Beliy_Rast
      self.Elektrougli = Elektrougli
      self.Vorsino = Vorsino
      self.Selyatino = Selyatino
      self.Khovrino = Khovrino
      self.Ramenskoye = Ramenskoye
      self.Lyubertsy = Lyubertsy


class InitialValues(Base):     #object при множестве таблиц
   __tablename__ = 'i_values'
   
   id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
   user_id: Mapped[int] = mapped_column(Integer, nullable=False)
   the_number_of_days_of_downtime_at_the_station: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   idle_time_at_the_terminal_before_loading: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_cost_of_downtime_on_pnop: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_cost_of_the_car: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   travel_time_to_the_station_on_the_railway_network: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   throwing_time_on_request: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   empty_mileage_distance: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   year_of_indexing: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   travel_time_to_the_terminal: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   
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
   the_rate_is_beyond_the_stop_on_unloading_19_1: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_is_beyond_the_stop_on_unloading_19_25_1: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_is_beyond_the_stop_on_unloading_25_1: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_is_beyond_the_stop_on_unloading_19_2: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_is_beyond_the_stop_on_unloading_19_25_2: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_is_beyond_the_stop_on_unloading_25_2: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_on_the_railway_tracks_19_1: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_on_the_railway_tracks_19_25_1: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_on_the_railway_tracks_25_1: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_on_the_railway_tracks_19_2: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_on_the_railway_tracks_19_25_2: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_on_the_railway_tracks_25_2: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   the_rate_for_downtime_at_the_pnop_at_the_unloading_station: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   idle_time_on_the_pnop_in_the_sludge_on_the_railway_network: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
   
   def __init__(
      self,
      user_id,
      the_rate_is_beyond_the_stop_on_unloading_19_1,
      the_rate_is_beyond_the_stop_on_unloading_19_25_1,
      the_rate_is_beyond_the_stop_on_unloading_25_1,
      the_rate_is_beyond_the_stop_on_unloading_19_2,
      the_rate_is_beyond_the_stop_on_unloading_19_25_2,
      the_rate_is_beyond_the_stop_on_unloading_25_2,
      the_rate_on_the_railway_tracks_19_1,
      the_rate_on_the_railway_tracks_19_25_1,
      the_rate_on_the_railway_tracks_25_1,
      the_rate_on_the_railway_tracks_19_2,
      the_rate_on_the_railway_tracks_19_25_2,
      the_rate_on_the_railway_tracks_25_2,
      the_rate_for_downtime_at_the_pnop_at_the_unloading_station,
      idle_time_on_the_pnop_in_the_sludge_on_the_railway_network
   ):
      self.user_id = user_id
      self.the_rate_is_beyond_the_stop_on_unloading_19_1 = the_rate_is_beyond_the_stop_on_unloading_19_1
      self.the_rate_is_beyond_the_stop_on_unloading_19_25_1 = the_rate_is_beyond_the_stop_on_unloading_19_25_1
      self.the_rate_is_beyond_the_stop_on_unloading_25_1 = the_rate_is_beyond_the_stop_on_unloading_25_1
      self.the_rate_is_beyond_the_stop_on_unloading_19_2 = the_rate_is_beyond_the_stop_on_unloading_19_2
      self.the_rate_is_beyond_the_stop_on_unloading_19_25_2 = the_rate_is_beyond_the_stop_on_unloading_19_25_2
      self.the_rate_is_beyond_the_stop_on_unloading_25_2 = the_rate_is_beyond_the_stop_on_unloading_25_2
      self.the_rate_on_the_railway_tracks_19_1 = the_rate_on_the_railway_tracks_19_1
      self.the_rate_on_the_railway_tracks_19_25_1 = the_rate_on_the_railway_tracks_19_25_1
      self.the_rate_on_the_railway_tracks_25_1 = the_rate_on_the_railway_tracks_25_1
      self.the_rate_on_the_railway_tracks_19_2 = the_rate_on_the_railway_tracks_19_2
      self.the_rate_on_the_railway_tracks_19_25_2 = the_rate_on_the_railway_tracks_19_25_2
      self.the_rate_on_the_railway_tracks_25_2 = the_rate_on_the_railway_tracks_25_2
      self.the_rate_for_downtime_at_the_pnop_at_the_unloading_station = the_rate_for_downtime_at_the_pnop_at_the_unloading_station
      self.idle_time_on_the_pnop_in_the_sludge_on_the_railway_network = idle_time_on_the_pnop_in_the_sludge_on_the_railway_network


# class InitialValuesBeliyRast(InitialValues, Base):
#    __tablename__ = 'i_values_Beliy_rast'


# class InitialValuesElektrougli(InitialValues, Base):
#    __tablename__ = 'i_values_Elektrougli'


# class InitialValuesVorsino(InitialValues, Base):
#    __tablename__ = 'i_values_Vorsino'


# class InitialValuesSelyatino(InitialValues, Base):
#    __tablename__ = 'i_values_Selyatino'


# class InitialValuesKhovrino(InitialValues, Base):
#    __tablename__ = 'i_values_Khovrino'


# class InitialValuesRamenskoye(InitialValues, Base):
#    __tablename__ = 'i_values_Ramenskoye'


# class InitialValuesLyubertsy(InitialValues, Base):
#    __tablename__ = 'i_values_Lyubertsy'