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


@app.get("/checkin", response_class = HTMLResponse)
async def checkin_page(request : Request):
    return templates.TemplateResponse(
        request = request, 
        name = "checkin.html", 
        context = {
            "user_dict" : user_dict
        }
    )

@app.post("/checkin", response_class = RedirectResponse)
async def enter_user(user_id : Annotated[int, Form()]):
    app.state.current_user = user_id
    return RedirectResponse(
        url = "/", 
        status_code=status.HTTP_302_FOUND
    )

@app.get("/", response_class = HTMLResponse)
async def display_home_page(request: Request):
    if app.state.current_user == 0:
        return RedirectResponse(
            url = "/checkin", 
            status_code=status.HTTP_302_FOUND
        )
    user_id = app.state.current_user
    user_name = user_dict[user_id]
    return templates.TemplateResponse(
        request = request, 
        name = "home.html", 
        context = {
            "user_id" : user_id,
            "current_user" : user_name
        }
    )

@app.get("/new_coffee_machine", response_class = HTMLResponse)
async def new_coffee_machine_page(request : Request):
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
    return templates.TemplateResponse(
        request = request, 
        name = "new_portafilter.html"
    )

@app.post("/new_portafilter", response_class = HTMLResponse)
async def enter_new_portafilter(
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
        return RedirectResponse(
            url = "/checkin", 
            status_code=status.HTTP_302_FOUND
        )
    
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
    request : Request,
    form_data : Annotated[EquipmentOwnership, Form()], 
    session : SessionDep
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

    context_dict = form_data.model_dump(mode = "json")
    context_dict["user_id"] = app.state.current_user
    context_dict["current_user"] = user_dict[app.state.current_user]

    return templates.TemplateResponse(
        request = request,
        name = "own_equipment.html",
        context = context_dict
    )

@app.get("/user_defaults", response_class = HTMLResponse)
async def user_defaults_page(request : Request, session : SessionDep):
    if app.state.current_user == 0:
        return RedirectResponse(
            url = "/checkin", 
            status_code=status.HTTP_302_FOUND
        )
    user_id = app.state.current_user
    user_name = user_dict[user_id]

    query = select(UserDefaults).where(UserDefaults.user_id == user_id)
    ex_default = session.exec(query).one()
    context_dict = ex_default.model_dump(mode = "json")
    
    machine_dict = get_coffee_machine_dict(user_id)
    machine_name = machine_dict[context_dict["coffee_machine_id"]]
    grinder_dict = get_grinder_dict(user_id)
    grinder_name = grinder_dict[context_dict["grinder_id"]]
    portafilter_dict = get_portafilter_dict(user_id)
    portafilter_name = portafilter_dict[context_dict["portafilter_id"]]

    context_dict["user_id"] = user_id
    context_dict["current_user"] = user_name
    context_dict["machine_name"] = machine_name
    context_dict["grinder_name"] = grinder_name
    context_dict["portafilter_name"] = portafilter_name
    context_dict["machine_dict"] = machine_dict
    context_dict["grinder_dict"] = grinder_dict
    context_dict["portafilter_dict"] = portafilter_dict

    return templates.TemplateResponse(
        request = request, 
        name = "user_defaults.html", 
        context = context_dict
    )

@app.post("/user_defaults", response_class = RedirectResponse)
async def enter_user_defaults(
    form_data : Annotated[UserDefaults, Form()], 
    session : SessionDep
):
    query = select(UserDefaults).where(UserDefaults.user_id == app.state.current_user)
    db_data = session.exec(query).one()
    subm_data = form_data.model_dump(exclude_unset = True)
    for key in subm_data:
        if subm_data[key] == "":
            subm_data[key] = None
    db_data.sqlmodel_update(subm_data)
    
    session.add(db_data)
    session.commit()
    session.refresh(db_data)

    return RedirectResponse(
        url = "/user_defaults",
        status_code = status.HTTP_302_FOUND
    )

@app.get("/new_coffee_beans", response_class = HTMLResponse)
async def new_coffee_bean_page(request : Request):
    return templates.TemplateResponse(
        request = request, 
        name = "new_coffee_beans.html"
    )

@app.post("/new_coffee_beans", response_class = HTMLResponse)
async def enter_new_coffee_bean(
        form_data : Annotated[CoffeeBeanVarieties, Form()],
        session : SessionDep, 
        request : Request
):
    session.add(form_data)
    session.commit()
    session.refresh(form_data)
    return templates.TemplateResponse(
        request = request, 
        name = "new_coffee_beans.html", 
        context = form_data.model_dump(mode = "json")
    )

@app.get("/new_coffee_purchase", response_class = HTMLResponse)
async def new_coffee_purchase_page(request : Request):
    if app.state.current_user == 0:
        return RedirectResponse(
            url = "/checkin", 
            status_code=status.HTTP_302_FOUND
        )
    
    user_id = app.state.current_user
    user_name = user_dict[user_id]
    variety_dict = get_all_coffees_dict()

    return templates.TemplateResponse(
        request = request, 
        name = "new_coffee_purchase.html", 
        context = {
            "user_id" : user_id,
            "current_user" : user_name, 
            "variety_dict" : variety_dict
        }
    )

@app.post("/new_coffee_purchase", response_class = HTMLResponse)
async def enter_new_coffee_purchase(
    request : Request,
    form_data : Annotated[CoffeeBeanPurchases, Form()], 
    session : SessionDep
):
    if form_data.roast_date == "":
        form_data.roast_date = None

    session.add(form_data)
    session.commit()
    session.refresh(form_data)

    user_id = app.state.current_user
    user_name = user_dict[user_id]
    variety_dict = get_all_coffees_dict()

    context_dict = form_data.model_dump(mode = "json")
    context_dict["user_id"] = user_id
    context_dict["current_user"] = user_name
    context_dict["variety_dict"] = variety_dict

    return templates.TemplateResponse(
        request = request, 
        name = "new_coffee_purchase.html", 
        context = context_dict
    )

@app.get("/new_experiment", response_class = HTMLResponse)
async def new_experiment_page(request : Request, session : SessionDep):
    if app.state.current_user == 0:
        return RedirectResponse(
            url = "/", 
            status_code=status.HTTP_302_FOUND
        )
    
    user_id = app.state.current_user
    user_name = user_dict[user_id]

    machine_dict = get_coffee_machine_dict(user_id)
    grinder_dict = get_grinder_dict(user_id)
    portafilter_dict = get_portafilter_dict(user_id)
    purchase_dict = get_purchase_dict(user_id)

    query = select(UserDefaults).where(UserDefaults.user_id == user_id)
    default_setup = session.exec(query).one()
    default_dict = default_setup.model_dump(mode = "json")

    context_dict = {}
    for key in default_dict:
        if default_dict[key] is None:
            default_dict[key] = ""
        context_dict["default_" + key] = default_dict[key]
    context_dict["user_id"] = user_id
    context_dict["current_user"] = user_name
    context_dict["machine_dict"] = machine_dict
    context_dict["grinder_dict"] = grinder_dict
    context_dict["portafilter_dict"] = portafilter_dict
    context_dict["purchase_dict"] = purchase_dict

    return templates.TemplateResponse(
        request = request, 
        name = "new_experiment.html",
        context = context_dict
    )

@app.post("/new_experiment", response_class = RedirectResponse)
async def enter_new_experiment(
    form_data : Annotated[EspressoExperiments, Form()], 
    session : SessionDep
):
    session.add(form_data)
    session.commit()
    session.refresh(form_data)
    return RedirectResponse(
        url = "/new_experiment/rate", 
        status_code=status.HTTP_302_FOUND
    )

@app.get("/new_experiment/rate", response_class = HTMLResponse)
async def experiment_rating_page(request : Request, session : SessionDep):
    if app.state.current_user == 0:
        return RedirectResponse(
            url = "/checkin", 
            status_code=status.HTTP_302_FOUND
        )
    
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
        name = "rate_experiment.html",
        context = context_dict
    )

@app.post("/new_experiment/rate", response_class = HTMLResponse)
async def enter_experiment_rating(
    request : Request,
    form_data : Annotated[EspressoExperiments, Form()], 
    session : SessionDep
):
    query = select(EspressoExperiments).where(EspressoExperiments.id == form_data.id)
    db_data = session.exec(query).one()
    subm_data = form_data.model_dump(exclude_unset = True)
    for key in subm_data:
        if subm_data[key] == "":
            subm_data[key] = None
    db_data.sqlmodel_update(subm_data)
    session.add(db_data)
    session.commit()
    session.refresh(db_data)

    context_dict = db_data.model_dump(mode = "json")
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
        name = "rate_experiment.html", 
        context = context_dict
    )
