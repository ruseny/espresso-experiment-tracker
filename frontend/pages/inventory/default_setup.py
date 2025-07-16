import streamlit as st
import requests
from datetime import datetime
from src.helpers import (
    get_user_defaults, 
    find_default_index,
    get_users_equipment_data,
    show_response_feedback
)

st.title("Default Setup")
st.write("Here you can edit your default setup that will be preselected for entering new espresso.")

user_defaults = get_user_defaults(
    user_id = st.session_state.current_user_id, 
    last_db_update = st.session_state.default_setup_db_update
)

with st.container(border = True):

    equipment_dicts = get_users_equipment_data(
        user_id = st.session_state.current_user_id,
        last_db_update = st.session_state.equipment_owned_db_update
    )
    
    st.header("Equipment")

    grinder_id = st.selectbox(
        "Grinder", 
        options = equipment_dicts["grinder_dict"],
        format_func = lambda x: equipment_dicts["grinder_dict"][x], 
        index = find_default_index(
            equipment_dicts["grinder_dict"], 
            user_defaults, 
            "grinder_id"
        )
    )

    coffee_machine_id = st.selectbox(
        "Coffee machine",
        options = equipment_dicts["machine_dict"],
        format_func = lambda x: equipment_dicts["machine_dict"][x], 
        index = find_default_index(
            equipment_dicts["machine_dict"], 
            user_defaults, 
            "coffee_machine_id"
        )
    )

with st.container(border = True):
    st.header("Portafilter")

    col1, col2 = st.columns(2)

    with col1:
        basket_pressurized = st.radio(
            "Pressurized basket?",
            options = ["yes", "no"],
            index = find_default_index(
                ["yes", "no"], 
                user_defaults, 
                "basket_pressurized"
            )
        )

        basket_shot_size = st.radio(
            "Basket shot size",
            options = ["single", "double"],
            index = find_default_index(
                ["single", "double"], 
                user_defaults, 
                "basket_shot_size"
            )
        )   

    with col2:
        portafilter_spout = st.radio(
            "Portafilter spout type",
            options = ["single", "double", "bottomless"],
            index = find_default_index(
                ["single", "double", "bottomless"], 
                user_defaults, 
                "portafilter_spout"
            )
        )

with st.container(border = True):

    st.header("Preparation details")

    col1, col2 = st.columns(2)

    with col1: 
        wdt_used = st.radio(
            "WDT used?", 
            options = ["yes", "no"], 
            index = find_default_index(
                ["yes", "no"], 
                user_defaults, 
                "wdt_used"
            )
        )

        tamping_method = st.radio(
            "Tamping method",
            options = ["manual", "electric"],
            index = find_default_index(
                ["manual", "electric"], 
                user_defaults, 
                "tamping_method"
            )
        )

        if tamping_method == "electric":
            tamping_weight_kg = st.number_input(
                "Tamping weight (kg)",
                min_value = 0,
                max_value = 50,
                value = user_defaults["tamping_weight_kg"]
            )
        else: 
            tamping_weight_kg = None

    with col2: 
        leveler_used = st.radio(
            "Leveler used?",
            options = ["yes", "no"],
            index = find_default_index(
                ["yes", "no"], 
                user_defaults, 
                "leveler_used"
            )
        )

        puck_screen_used = st.radio(
            "Puck screen used?",
            options = ["yes", "no"],
            index = find_default_index(
                ["yes", "no"], 
                user_defaults, 
                "puck_screen_used"
            )
        )

        if puck_screen_used == "yes":
            puck_screen_thickness_mm = st.number_input(
                "Puck screen thickness (mm)",
                min_value = 0.0,
                max_value = 10.0,
                value = user_defaults["puck_screen_thickness_mm"], 
                step = 0.1
            )
        else:
            puck_screen_thickness_mm = None

setup_name = st.text_input("Please (re)name your setup")

payload = {
    "user_id" : st.session_state.current_user_id,
    "grinder_id" : grinder_id,
    "coffee_machine_id" : coffee_machine_id,
    "basket_pressurized" : basket_pressurized,
    "basket_shot_size" : basket_shot_size,
    "portafilter_spout" : portafilter_spout,
    "wdt_used" : wdt_used,
    "tamping_method" : tamping_method,
    "tamping_weight_kg" : tamping_weight_kg,
    "leveler_used" : leveler_used,
    "puck_screen_used" : puck_screen_used,
    "puck_screen_thickness_mm" : puck_screen_thickness_mm,
    "setup_name" : setup_name
}

if user_defaults is None:
    st.write("No default setup found. Saving will create a new one.")
    if st.button ("Save new default settings", key = "save_post"):
        save_user_defaults_resp = requests.post(
            f"{st.session_state.backend_url}/user_defaults",
            json = payload
        )
        show_response_feedback(save_user_defaults_resp)
        if save_user_defaults_resp.status_code == 200:
            st.session_state.default_setup_db_update = datetime.now()
else:
    st.write("Saving will update the existing default settings.")
    if st.button ("Save changes", key = "save_put"):
        save_user_defaults_resp = requests.put(
            f"{st.session_state.backend_url}/user_defaults",
            json = payload
        )
        show_response_feedback(save_user_defaults_resp)
        if save_user_defaults_resp.status_code == 200:
            st.session_state.default_setup_db_update = datetime.now()