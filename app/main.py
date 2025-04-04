from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import status

from pydantic import BaseModel
from typing import Annotated

from datetime import date
import json


app = FastAPI()
templates = Jinja2Templates(directory = "../templates")

coffee_beans_list = ["Lavazza", "Segafredo", "Tchibo"]

# import mysql.connector
# mysql_db = mysql.connector.connect(
#     host = "localhost", 
#     user = "app_connection", 
#     password = "Z4r*95qTT$^SGwVV", 
#     database = "espresso_experiment_tracker"
# )
# db_cursor = mysql_db.cursor()


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
            "coffee_beans_list" : coffee_beans_list
        }
    )

class NewExperiment(BaseModel):
    equipment_setup_id : int = 1
    coffee_beans : str
    grind_setting : int
    dose_gr : float
    wdt_used : str = "yes"
    leveler_used : str = "no"
    puck_screen_used : str = "yes"
    extraction_time_sec : float
    # water_temp_c : Optional[int] = Form(None)
    yield_gr : float

@app.post("/new_experiment", response_class = RedirectResponse)
async def enter_new_experiment(
    request : Request, 
    form_data : Annotated[NewExperiment, Form()]
):
    with open("experiment_data.json", "w") as f:
        f.write(f"{form_data.model_dump_json()}")

    return RedirectResponse(url = "/show_experiment", status_code=status.HTTP_302_FOUND)