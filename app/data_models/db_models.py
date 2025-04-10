from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime

from .enum_defs import UserTypes, PidTypes, OperationTypes, YesNo, BasketSizes, SpoutTypes, OriginTypes, EqpTypes


class Users(SQLModel, table = True):
    __tablename__ = "Users"
    id : Optional[int] = Field(default = None, primary_key = True)
    username : str = Field(default = None)
    # password_hash : str = Field(default = None)
    # email : str = Field(default = None)
    first_name : Optional[str] = Field(default = None)
    last_name : Optional[str] = Field(default = None)
    date_of_birth : Optional[date] = Field(default = None)
    registration_datetime : datetime = Field(default_factory = datetime.now)
    user_type : UserTypes = Field(default = "developer")

class CoffeeMachines(SQLModel, table = True):
    __tablename__ = "CoffeeMachines"
    id : Optional[int] = Field(default = None, primary_key = True)
    manufacturer : str = Field(default = None)
    model_name : str = Field(default = None)
    model_name_add : Optional[str] = Field(default = None)
    model_specification : Optional[str] = Field(default = None)
    model_serial : str = Field(default = None)
    pump_pressure_bar : int = Field(default = None)
    pump_type : Optional[str] = Field(default = None)
    water_temp_control : Optional[str] = Field(default = None)
    pid_control : PidTypes = Field(default = "")
    boiler_type : Optional[str] = Field(default = None)
    portafilter_diam_mm : int = Field(default = None)

class Grinders(SQLModel, table = True):
    __tablename__ = "Grinders"
    id : Optional[int] = Field(default = None, primary_key = True)
    manufacturer : str = Field(default = None)
    model_name : str = Field(default = None)
    model_name_add : Optional[str] = Field(default = None)
    model_specification : Optional[str] = Field(default = None)
    model_serial : str = Field(default = None)
    operation_type : OperationTypes = Field(default = None)
    burr_shape : Optional[str] = Field(default = None)
    burr_diameter_mm : Optional[int] = Field(default = None)
    burr_material : Optional[str] = Field(default = None)
    min_fine_setting : Optional[int] = Field(default = None)
    max_fine_setting : Optional[int] = Field(default = None)
    min_coarse_setting : Optional[int] = Field(default = None)
    max_coarse_setting : Optional[int] = Field(default = None)
    single_dose : YesNo = Field(default = "no")

class Portafilters(SQLModel, table = True):
    __tablename__ = "Portafilters"
    id : Optional[int] = Field(default = None, primary_key = True)
    manufacturer : str = Field(default = None)
    model_name : str = Field(default = None)
    model_name_add : Optional[str] = Field(default = None)
    model_specification : Optional[str] = Field(default = None)
    model_serial : str = Field(default = None)
    basket_diameter_mm : int = Field(default = None)
    pressurized : YesNo = Field(default = "no")
    basket_shot_size : BasketSizes = Field(default = None)
    spout : SpoutTypes = Field(default = None)

class EquipmentOwnership(SQLModel, table = True):
    __tablename__ = "EquipmentOwnership"
    id : Optional[int] = Field(default = None, primary_key = True)
    user_id : int = Field(default = None, foreign_key = "Users.id")
    equipment_type : EqpTypes = Field(default = None)
    coffee_machine_id : Optional[int] = Field(default = None, foreign_key = "CoffeeMachines.id")
    grinder_id : Optional[int] = Field(default = None, foreign_key = "Grinders.id")
    portafilter_id : Optional[int] = Field(default = None, foreign_key = "Portafilters.id")
    purchase_date : Optional[date] = Field(default = None)
    purchased_from : Optional[str] = Field(default = None)
    purchace_price_eur : Optional[float] = Field(default = None)

class UserDefaults(SQLModel, table = True):
    __tablename__ = "UserDefaults"
    user_id : int = Field(default = None, primary_key = True, foreign_key = "Users.id")
    coffee_machine_id : int = Field(default = 1, foreign_key = "CoffeeMachines.id")
    grinder_id : int = Field(default = 1, foreign_key = "Grinders.id")
    portafilter_id : int = Field(default = 1, foreign_key = "Portafilters.id")
    wdt_used : YesNo = Field(default = "no")
    tamping_method : OperationTypes = Field(default = "manual")
    tamping_weight_kg : Optional[float] = Field(default = None)
    leveler_used : YesNo = Field(default = "no")   
    puck_screen_used : YesNo = Field(default = "no")
    puck_screen_thickness_mm : Optional[float] = Field(default = None)
    setup_name : Optional[str] = Field(default = None)

class CoffeeBeanVarieties(SQLModel, table = True):
    __tablename__ = "CoffeeBeanVarieties"
    id : Optional[int] = Field(default = None, primary_key = True)
    producer : str = Field(default = None)
    name : str = Field(default = None)
    origin : Optional[str] = Field(default = None)
    origin_type : OriginTypes = Field(default = None)
    arabica_ratio : Optional[float] = Field(default = None)
    roast_level : Optional[float] = Field(default = None)
    intensity : Optional[float] = Field(default = None)
    acidity : Optional[float] = Field(default = None)
    flavor_notes : Optional[str] = Field(default = None)
    decaffeinated : YesNo = Field(default = "no")

class CoffeeBeanPurchases(SQLModel, table = True):
    __tablename__ = "CoffeeBeanPurchases"
    id : Optional[int] = Field(default = None, primary_key = True)
    user_id : int = Field(default = 1, foreign_key = "Users.id")
    variety_id : int = Field(default = 1, foreign_key = "CoffeeBeanVarieties.id")
    purchase_date : date = Field(default_factory = date.today)
    purchased_from : str = Field(default = None)
    roast_date : date = Field(default = None)
    weight_kg : float = Field(default = None)
    price_per_kg_eur : float = Field(default = None)

class EspressoExperiments(SQLModel, table = True):
    __tablename__ = "EspressoExperiments"
    id : Optional[int] = Field(default=None, primary_key=True)
    user_id : int = Field(default = None, foreign_key = "Users.id")
    experiment_datetime : datetime = Field(default_factory = datetime.now)
    coffee_machine_id : int = Field(default = None, foreign_key = "CoffeeMachines.id")
    grinder_id : int = Field(default = None, foreign_key = "Grinders.id")
    portafilter_id : int = Field(default = None, foreign_key = "Portafilters.id")
    wdt_used : YesNo = Field(default = "no")
    tamping_method : OperationTypes = Field(default = "manual")
    tamping_weight_kg : Optional[float] = Field(default = None)
    leveler_used : YesNo = Field(default = "no")   
    puck_screen_used : YesNo = Field(default = "no")
    puck_screen_thickness_mm : Optional[float] = Field(default = None)
    coffee_bean_purchase_id : int = Field(default = None, foreign_key = "CoffeeBeanPurchases.id")
    grind_setting : int = Field(default = None)
    dose_gr : float = Field(default = None)
    water_temp_c : Optional[int] = Field(default = 93)
    extraction_time_sec : int = Field(default = None)
    yield_gr : float = Field(default = None)
    evaluation_general : Optional[int] = Field(default = None, ge = 1, le = 10)
    evaluation_flavor : Optional[int] = Field(default = None, ge = 1, le = 10)
    evaluation_body : Optional[int] = Field(default = None, ge = 1, le = 10)
    evaluation_crema : Optional[int] = Field(default = None, ge = 1, le = 10)
    evaluation_notes : Optional[str] = Field(default = None)
