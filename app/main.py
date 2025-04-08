from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from typing import Annotated

from .dependecies.db_session import SessionDep
from .data_models.db_models import EspressoExperiments


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
async def display_experiment_page(request : Request, session : SessionDep):
    query = select(EspressoExperiments).order_by(EspressoExperiments.id.desc()).limit(1)
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
    form_data : Annotated[EspressoExperiments, Form()], 
    session : SessionDep
):
    session.add(form_data)
    session.commit()
    session.refresh(form_data)
    return RedirectResponse(url = "/show_experiment", status_code=status.HTTP_302_FOUND)