from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import status

from sqlmodel import Field, Session, SQLModel, create_engine, select
from enum import Enum

from pydantic import BaseModel
from typing import Annotated, List, Literal, Optional

from datetime import datetime, date
import json


app = FastAPI()
templates = Jinja2Templates(directory = "../templates")

coffee_beans_purchase_mapper = {1 : "Lavazza", 2 : "Segafredo", 3 : "Tchibo"}



@app.get("/", response_class = HTMLResponse)
async def display_home_page(request: Request):
    return templates.TemplateResponse(
        request = request, 
        name = "home.html"
    )

@app.get("/show_experiment", response_class = HTMLResponse)
async def display_experiment_page(request : Request):
    with open("experiment_data.json", "r") as f:
        experiment_data = json.load(f)
    return templates.TemplateResponse(
        request = request, 
        name = "show_experiment.html",
        context = experiment_data
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

class YesNo(str, Enum):
    yes = "yes"
    no = "no"

class EspressoExperiments(SQLModel, table = True):
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

@app.post("/new_experiment", response_class = RedirectResponse)
async def enter_new_experiment(
    request : Request, 
    form_data : Annotated[EspressoExperiments, Form()]
):
    with open("experiment_data.json", "w") as f:
        f.write(f"{form_data.model_dump_json()}")

    return RedirectResponse(url = "/show_experiment", status_code=status.HTTP_302_FOUND)