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
from .data_models.db_models import *
from .crud.selection_dicts import *

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
    context_dict = last_entry.model_dump(mode = "json")

    user_id = context_dict["user_id"]
    user_name = user_dict[context_dict["user_id"]]

    machine_dict = get_coffee_machine_dict(user_id)
    machine_name = machine_dict[context_dict["coffee_machine_id"]]
    grinder_dict = get_grinder_dict(user_id)
    grinder_name = grinder_dict[context_dict["grinder_id"]]
    portafilter_dict = get_portafilter_dict(user_id)
    portafilter_name = portafilter_dict[context_dict["portafilter_id"]]
    purchase_dict = get_purchase_dict(user_id)
    coffee_name = purchase_dict[context_dict["coffee_bean_purchase_id"]]

    context_dict["user_name"] = user_name
    context_dict["machine_name"] = machine_name
    context_dict["grinder_name"] = grinder_name
    context_dict["portafilter_name"] = portafilter_name
    context_dict["coffee_name"] = coffee_name

    return templates.TemplateResponse(
        request = request, 
        name = "show_experiment.html",
        context = context_dict
    )

@app.get("/new_experiment", response_class = HTMLResponse)
async def new_experiment_page(request : Request):
    if app.state.current_user == 0:
        return RedirectResponse(url = "/", status_code=status.HTTP_302_FOUND)
    user_id = app.state.current_user
    user_name = user_dict[user_id]
    machine_dict = get_coffee_machine_dict(user_id)
    grinder_dict = get_grinder_dict(user_id)
    portafilter_dict = get_portafilter_dict(user_id)
    purchase_dict = get_purchase_dict(user_id)
    return templates.TemplateResponse(
        request = request, 
        name = "new_experiment.html",
        context = {
            "user_id" : user_id,
            "current_user" : user_name, 
            "machine_dict" : machine_dict,
            "grinder_dict" : grinder_dict,
            "portafilter_dict" : portafilter_dict,
            "purchase_dict" : purchase_dict,
            "water_temp_c" : 93
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

@app.get("/new_coffee_machine", response_class = HTMLResponse)
async def new_coffee_machine_page(request : Request):
    if app.state.current_user == 0:
        return RedirectResponse(url = "/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        request = request, 
        name = "new_coffee_machine.html"
    )

@app.post("/new_coffee_machine", response_class = HTMLResponse)
async def enter_new_coffee_machine(
        form_data : Annotated[CoffeeMachines, Form()],
        session : SessionDep, 
        request : Request
):
    session.add(form_data)
    session.commit()
    session.refresh(form_data)
    return templates.TemplateResponse(
        request = request, 
        name = "new_coffee_machine.html", 
        context = form_data.model_dump(mode = "json")
    )

@app.get("/new_grinder", response_class = HTMLResponse)
async def new_grinder_page(request : Request):
    if app.state.current_user == 0:
        return RedirectResponse(url = "/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        request = request, 
        name = "new_grinder.html"
    )

@app.post("/new_grinder", response_class = HTMLResponse)
async def enter_new_grinder(
        form_data : Annotated[Grinders, Form()],
        session : SessionDep, 
        request : Request
):
    session.add(form_data)
    session.commit()
    session.refresh(form_data)
    return templates.TemplateResponse(
        request = request, 
        name = "new_grinder.html", 
        context = form_data.model_dump(mode = "json")
    )

@app.get("/new_portafilter", response_class = HTMLResponse)
async def new_portafilter_page(request : Request):
    if app.state.current_user == 0:
        return RedirectResponse(url = "/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        request = request, 
        name = "new_portafilter.html"
    )

@app.post("/new_portafilter", response_class = HTMLResponse)
async def enter_new_grinder(
        form_data : Annotated[Portafilters, Form()],
        session : SessionDep, 
        request : Request
):
    session.add(form_data)
    session.commit()
    session.refresh(form_data)
    return templates.TemplateResponse(
        request = request, 
        name = "new_portafilter.html", 
        context = form_data.model_dump(mode = "json")
    )

@app.get("/own_equipment", response_class = HTMLResponse)
async def owned_equipment_page(request : Request):
    if app.state.current_user == 0:
        return RedirectResponse(url = "/", status_code=status.HTTP_302_FOUND)
    user_id = app.state.current_user
    user_name = user_dict[user_id]
    machine_dict = get_all_coffee_machines_dict()
    grinder_dict = get_all_grinders_dict()
    portafilter_dict = get_all_portafilters_dict()
    return templates.TemplateResponse(
        request = request, 
        name = "own_equipment.html",
        context = {
            "user_id" : user_id,
            "current_user" : user_name, 
            "machine_dict" : machine_dict,
            "grinder_dict" : grinder_dict,
            "portafilter_dict" : portafilter_dict
        }
    )

@app.post("/own_equipment", response_class = HTMLResponse)
async def enter_owned_equipment(
    form_data : Annotated[EquipmentOwnership, Form()], 
    session : SessionDep,
    request : Request
):
    if form_data.equipment_type == "coffee machine":
        form_data.grinder_id = None
        form_data.portafilter_id = None
    elif form_data.equipment_type == "grinder":
        form_data.coffee_machine_id = None
        form_data.portafilter_id = None
    elif form_data.equipment_type == "portafilter":
        form_data.coffee_machine_id = None
        form_data.grinder_id = None

    session.add(form_data)
    session.commit()
    session.refresh(form_data)
    return templates.TemplateResponse(
        request = request, 
        name = "own_equipment.html", 
        context = form_data.model_dump(mode = "json")
    )