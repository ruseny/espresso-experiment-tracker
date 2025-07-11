"""
App for tracking espresso experiments.
"""

# Library imports
from fastapi import FastAPI, Query
from sqlmodel import select
from typing import Annotated

# Local module imports:
from dependency_inj.db_session import SessionDep
from data_models.db_models import *
from crud.get_requests import *

# Initialise app
app = FastAPI()

# Persist last checked in user
app.state.current_user = 0
user_dict = get_user_dict()

#############
# ENDPOINTS #
#############

# User check-in #####################################
@app.get("/users/")
async def send_user_list() -> dict:
    return get_user_dict()

@app.post("/users/{user_id}")
async def check_in_user(user_id : int):
    app.state.current_user = user_id
    return {"message" : "User update successful."}
######################################################

# User's lists #######################################
@app.get("/equipment/{user_id}")
async def send_equipment_data(user_id : int) -> dict:
    machine_dict = get_coffee_machine_dict(user_id)
    grinder_dict = get_grinder_dict(user_id)
    return {
        "machine_dict" : machine_dict,
        "grinder_dict" : grinder_dict
    }

@app.get("/coffee/producers/{user_id}")
async def send_producer_data(
    user_id : int, 
    time_frame : int = 30, 
    max_items : int = 10
) -> dict:
    producer_list = get_producer_list(
        user_id = user_id, 
        time_frame = time_frame, 
        max_items = max_items
    )
    return {"producer_list" : producer_list}

@app.get("/coffee/purchases/{user_id}")
async def send_coffe_purchase_data(
    user_id : int, 
    time_frame : int = 30,
    max_items : int = 10, 
    producers : Annotated[list, Query()] = None
) -> dict:
    return get_purchase_dict(
        user_id = user_id,
        time_frame = time_frame,
        max_items = max_items,
        producers = producers
    )
######################################################

# User defaults #######################################
@app.get("/user_defaults/{user_id}")
async def send_defaults_data(user_id : int) -> dict:
    return get_user_defaults_dict(user_id)

@app.post("/user_defaults/")
async def save_user_defaults(
    default_setup_data: UserDefaults, 
    session : SessionDep
) -> dict:
    session.add(default_setup_data)
    session.commit()
    session.refresh(default_setup_data)
    return {"message" : "User defaults saved successfully."}

@app.put("/user_defaults/")
async def update_user_defaults(
    defaults_data: UserDefaults, 
    session : SessionDep
) -> dict:
    query = select(UserDefaults).where(
        UserDefaults.user_id == defaults_data.user_id
    )
    db_data = session.exec(query).one()
    subm_data = defaults_data.model_dump(exclude_unset = True)
    db_data.sqlmodel_update(subm_data)
    
    session.add(db_data)
    session.commit()
    session.refresh(db_data)

    return {"message" : "User defaults updated successfully."}
################################################################

# Espresso making ####################################################
@app.post("/new_espresso/save_espresso/")
async def save_new_espresso(
    espresso_data : EspressoExperiments, 
    session : SessionDep
) -> dict:
    session.add(espresso_data)
    session.commit()
    session.refresh(espresso_data)

    last_experiment = get_users_last_experiment(
        user_id = espresso_data.user_id
    )

    return {
        "message" : "Espresso data saved successfully.",
        "id" : last_experiment["id"], 
        "experiment_datetime" : last_experiment["experiment_datetime"]
    }

@app.patch("/new_espresso/save_espresso/evaluate/")
async def evaluate_espresso(
    eval_data : EspressoExperiments, 
    session : SessionDep
) -> dict:
    query = select(EspressoExperiments).where(
        EspressoExperiments.id == eval_data.id
    )
    db_data = session.exec(query).one()
    subm_data = eval_data.model_dump(exclude_unset = True)
    db_data.sqlmodel_update(subm_data)
    
    session.add(db_data)
    session.commit()
    session.refresh(db_data)

    return {"message" : "Evaluation has been saved successfully."}
#######################################################################

# Full lists ##########################################################
@app.get("/coffee/all_varieties/")
async def send_all_coffee_varieties(
    producers : Annotated[list, Query()] = None
) -> dict:
    return get_all_coffees_dict(producers = producers)

@app.get("/coffee/all_sellers/")
async def send_all_sellers() -> dict:
    return {"sellers_list" : get_all_sellers_list()}

@app.get("/coffee/all_producers/")
async def send_all_producers() -> dict:
    return {"producers_list" : get_all_producers_list()}

@app.get("/equipment/coffee_machines/")
async def send_all_coffee_machines(
    manufacturers : Annotated[list, Query()] = None
) -> dict:
    return get_all_coffee_machines_dict(manufacturers = manufacturers)

@app.get("/equipment/coffee_machine_manufacturers/")
async def send_all_coffee_machine_manufacturers() -> dict:
    return {"manufacturers" : get_all_coffee_machine_manufacturers()}

@app.get("/equipment/grinders/")
async def send_all_grinders(
    manufacturers : Annotated[list, Query()] = None
) -> dict:
    return get_all_grinders_dict(manufacturers = manufacturers)

@app.get("/equipment/grinder_manufacturers/")
async def send_all_grinder_manufacturers() -> dict:
    return {"manufacturers" : get_all_grinder_manufacturers()}

@app.get("/equipment/all_sellers/")
async def send_all_equipment_sellers() -> dict:
    return {"sellers" : get_all_equipment_sellers_list()}
#######################################################################

# Save coffee #########################################################
@app.post("/coffee/purchases/save_new/")
async def save_new_coffee_purchase(
    purchase_data : CoffeeBeanPurchases,
    session : SessionDep
) -> dict:
    session.add(purchase_data)
    session.commit()
    session.refresh(purchase_data)

    return {"message" : "Coffee purchase data saved successfully."}

@app.post("/coffee/varieties/save_new/")
async def save_new_coffee_variety(
    variety_data : CoffeeBeanVarieties, 
    session : SessionDep
) -> dict:
    session.add(variety_data)
    session.commit()
    session.refresh(variety_data)

    return {"message" : "Coffee variety data saved successfully."}
#######################################################################

# Equipment ###########################################################
@app.post("/equipment/add_owned_equipment/")
async def add_owned_equipment(
    equipment_data : EquipmentOwnership,
    session : SessionDep
) -> dict:
    session.add(equipment_data)
    session.commit()
    session.refresh(equipment_data)

    return {"message" : "Equipment ownership data saved successfully."}

@app.post("/equipment/save_new_coffee_machine/")
async def save_new_coffee_machine(
    coffee_machine_data : CoffeeMachines,
    session : SessionDep
) -> dict:
    session.add(coffee_machine_data)
    session.commit()
    session.refresh(coffee_machine_data)

    return {"message" : "Coffee machine data saved successfully."}

@app.post("/equipment/save_new_grinder/")
async def save_new_grinder(
    grinder_data : Grinders,
    session : SessionDep
) -> dict:
    session.add(grinder_data)
    session.commit()
    session.refresh(grinder_data)

    return {"message" : "Grinder data saved successfully."}

########################################################################

# Lists from espresso data #########################################
@app.get("/espresso_data/filter_default_range/{user_id}")
async def send_filter_default_range(user_id : int) -> dict:
    return get_espresso_filter_default_range(user_id)

@app.get("/espresso_data/coffee_list/{user_id}")
async def send_coffee_dict_from_espresso(user_id : int) -> dict:
    return get_coffee_dict_from_espresso(user_id) 

# Run app with uvicorn, set port and host ##############################

if __name__ == "__main__":
    import uvicorn
    import os
    from dotenv import load_dotenv

    load_dotenv()

    host = "127.0.0.1"
    port = 8601

    uvicorn.run("main:app", host=host, port=port, reload=True)

