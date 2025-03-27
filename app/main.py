from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from typing import Annotated

from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory = "../templates")

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.get("/", response_class = HTMLResponse)
async def display_home_page(request: Request):
    return templates.TemplateResponse(
        request = request, 
        name = "home.html", 
        context = {
            "current_time" : current_time
        }
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
        name = "new_experiment.html"
    )

@app.post("/new_experiment", response_class = HTMLResponse)
async def enter_new_experiment(
    request : Request, 
    coffee_beans : Annotated[str, Form()],
    grind_level : Annotated[int, Form()], 
    amount_gr : Annotated[float, Form()], 
    extr_time_sec : Annotated[int, Form()], 
    outp_ml : Annotated[float, Form()]
):
    
    extr_ratio = round(outp_ml / amount_gr, 2)

    if extr_time_sec < 25:
        extr_time_message = "Too short extraction time"
    elif extr_time_sec > 30:
        extr_time_message = "Too long extraction time"
    else:
        extr_time_message = "Good extraction time"

    return templates.TemplateResponse(
        request = request, 
        name = "new_experiment.html", 
        context = {
            "coffee_beans" : coffee_beans,
            "grind_level" : grind_level,
            "amount_gr" : amount_gr,
            "extr_time_sec" : extr_time_sec,
            "outp_ml" : outp_ml,
            "extr_ratio" : extr_ratio, 
            "extr_time_message" : extr_time_message
        }
    )