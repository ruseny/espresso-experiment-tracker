from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from typing import Annotated


app = FastAPI()
templates = Jinja2Templates(directory = "../templates")

coffee_beans_list = ["Lavazza", "Segafredo", "Tchibo"]


@app.get("/", response_class = HTMLResponse)
async def display_home_page(request: Request):
    return templates.TemplateResponse(
        request = request, 
        name = "home.html"
    )

@app.get("/show_experiment", response_class = HTMLResponse)
async def display_experiment_page(request : Request, id : int = 0):
    return templates.TemplateResponse(
        request = request, 
        name = "show_experiment.html",
        context = {
            "experiment_id" : id
        }
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
    coffee_beans : str
    grind_level : int
    amount_gr : float
    extr_time_sec : float
    outp_ml : float

@app.post("/new_experiment", response_class = HTMLResponse)
async def enter_new_experiment(
    request : Request, 
    form_data : Annotated[NewExperiment, Form()]
):
    
    extr_ratio = round(form_data.outp_ml / form_data.amount_gr, 2)

    if form_data.extr_time_sec < 25:
        extr_time_message = "Too short extraction time"
    elif form_data.extr_time_sec > 30:
        extr_time_message = "Too long extraction time"
    else:
        extr_time_message = "Good extraction time"

    return templates.TemplateResponse(
        request = request, 
        name = "new_experiment.html", 
        context = {
            "coffee_beans_list" : coffee_beans_list, 
            "coffee_beans" : form_data.coffee_beans,
            "grind_level" : form_data.grind_level,
            "amount_gr" : form_data.amount_gr,
            "extr_time_sec" : form_data.extr_time_sec,
            "outp_ml" : form_data.outp_ml,
            "extr_ratio" : extr_ratio, 
            "extr_time_message" : extr_time_message
        }
    )