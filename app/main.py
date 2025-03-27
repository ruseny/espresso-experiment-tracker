from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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