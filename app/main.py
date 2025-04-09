"""
App for tracking espresso experiments.
"""

# Library imports
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from typing import Annotated

# Local module imports:
from .dependencies.db_session import SessionDep
from .data_models.db_models import EspressoExperiments
from .crud.selection_dicts import get_purchase_dict, get_user_dict, get_setup_dict

# Initialise app and frontend
app = FastAPI()
templates = Jinja2Templates(directory = "../templates")

# Variables to share across requests
app.state.current_user = 0
user_dict = get_user_dict()


@app.get("/", response_class = HTMLResponse)
async def display_home_page(request: Request):
    return templates.TemplateResponse(
        request = request, 
        name = "home.html", 
        context = {
            "user_dict" : user_dict
        }
    )

@app.post("/", response_class = RedirectResponse)
async def enter_user(user_id : Annotated[int, Form()]):
    app.state.current_user = user_id
    return RedirectResponse(url = "/new_experiment", status_code=status.HTTP_302_FOUND)

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
    if app.state.current_user == 0:
        return RedirectResponse(url = "/", status_code=status.HTTP_302_FOUND)
    user_name = user_dict[app.state.current_user]
    purchase_dict = get_purchase_dict(user_id = app.state.current_user)
    setup_dict = get_setup_dict(user_id = app.state.current_user)
    return templates.TemplateResponse(
        request = request, 
        name = "new_experiment.html",
        context = {
            "current_user" : user_name, 
            "purchase_dict" : purchase_dict,
            "setup_dict" : setup_dict, 
            "water_temp_c" : 93, 
            "leveler_used" : "no"
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