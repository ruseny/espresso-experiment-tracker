from enum import Enum
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime
 

class YesNo(str, Enum):
    yes = "yes"
    no = "no"

class EspressoExperiments(SQLModel, table = True):
    __tablename__ = "EspressoExperiments"
    id : Optional[int] = Field(default=None, primary_key=True)
    experiment_datetime : datetime = Field(default_factory = datetime.now)
    setup_id : int = Field(default = 1, foreign_key = "EquipmentSetup.id")
    coffee_bean_purchase_id : int = Field(default = None, foreign_key = "CoffeeBeanPurchases.id")
    grind_setting : int = Field(default = None)
    dose_gr : float = Field(default = None)
    wdt_used : YesNo = Field(default = "yes")
    leveler_used : YesNo = Field(default = "no")
    puck_screen_used : YesNo = Field(default = "yes")
    extraction_time_sec : int = Field(default = None)
    water_temp_c : Optional[int] = Field(default = 93)
    yield_gr : float = Field(default = None)
    evaluation_general : Optional[int] = Field(default = None, ge = 1, le = 10)
    evaluation_flavor : Optional[int] = Field(default = None, ge = 1, le = 10)
    evaluation_body : Optional[int] = Field(default = None, ge = 1, le = 10)
    evaluation_crema : Optional[int] = Field(default = None, ge = 1, le = 10)
    evaluation_notes : Optional[str] = Field(default = None)

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

class EquipmentSetup(SQLModel, table = True):
    __tablename__ = "EquipmentSetup"
    id : Optional[int] = Field(default = None, primary_key = True)
    user_id : int = Field(default = 1, foreign_key = "Users.id")
    coffee_machine_id : int = Field(default = 1, foreign_key = "EspressoMachines.id")
    grinder_id : int = Field(default = 1, foreign_key = "Grinders.id")
    portafilter_id : int = Field(default = 1, foreign_key = "WaterFilters.id")
    setup_name : Optional[str] = Field(default = None)