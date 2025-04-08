from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import status

from sqlmodel import Field, Session, SQLModel, create_engine, text, select
from enum import Enum

from pydantic import BaseModel
from typing import Annotated, List, Literal, Optional

from datetime import datetime, date
import json


app = FastAPI()
templates = Jinja2Templates(directory = "../templates")

coffee_beans_purchase_mapper = {1 : "Lavazza", 2 : "Segafredo", 3 : "Tchibo"}

with open("credentials/db_login.json", "r") as f:
    db_login = json.load(f)
db_path = f"mysql://{db_login['user']}:{db_login['password']}@{db_login['host']}/{db_login['db_name']}"
db_engine = create_engine(db_path)
def get_session():
    with Session(db_engine) as session:
        yield session
SessionDep = Annotated[Session, Depends(get_session)]

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



@app.get("/", response_class = HTMLResponse)
async def display_home_page(request: Request):
    return templates.TemplateResponse(
        request = request, 
        name = "home.html"
    )

@app.get("/show_experiment", response_class = HTMLResponse)
async def display_experiment_page(
    request : Request, 
    session : SessionDep
):
    query = select(EspressoExperiments).order_by(EspressoExperiments.experiment_datetime.desc()).limit(1)
    last_entry = session.exec(query).one()
    return templates.TemplateResponse(
        request = request, 
        name = "show_experiment.html",
        context = last_entry.model_dump(mode = "json")
    )

@app.get("/new_experiment", response_class = HTMLResponse)
async def new_experiment_page(request : Request):
    return templates.TemplateResponse(
        request = request, 
        name = "new_experiment.html",
        context = {
            "coffee_beans_purchase_mapper" : coffee_beans_purchase_mapper
        }
    )




@app.post("/new_experiment", response_class = RedirectResponse)
async def enter_new_experiment(
    request : Request, 
    form_data : Annotated[EspressoExperiments, Form()],
    session : SessionDep
):
    session.add(form_data)
    session.commit()
    session.refresh(form_data)

    return RedirectResponse(url = "/show_experiment", status_code=status.HTTP_302_FOUND)