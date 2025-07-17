import streamlit as st
import requests
from datetime import date, timedelta
from frontend.src.api_requests import (
    get_user_defaults, 
    find_default_index,
    get_users_equipment_data,
    get_users_coffee_producer_list,
    get_users_coffee_data, 
    show_response_feedback
)

st.title("New Espresso")

user_defaults = get_user_defaults(
    user_id = st.session_state.current_user_id, 
    last_db_update = st.session_state.default_setup_db_update)

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
    
    st.header("Coffee")

    with st.expander("Filter selection"):
        with st.form("coffee_purchase_filters", border = False):
            col1, col2 = st.columns(2)

            with col1:
                purchased_since = st.date_input(
                    "Purchases since",
                    value = date.today() - timedelta(days = 30),
                    min_value = date.today() - timedelta(days = 730)
                )
                time_frame = (date.today() - purchased_since).days

            with col2:
                max_items = st.number_input(
                    "Maximum items to display",
                    min_value = 1,
                    max_value = 100,
                    value = 10
                )

            producer_list = get_users_coffee_producer_list(
                user_id = st.session_state.current_user_id, 
                last_db_update = st.session_state.coffee_purchase_db_update,
                time_frame = time_frame,
                max_items = max_items
            )["producer_list"]

            producers = st.multiselect(
                "Producers",
                options = producer_list,
                default = producer_list
            )

            st.form_submit_button("Apply filters")
        
    coffee_dict = get_users_coffee_data(
        user_id = st.session_state.current_user_id, 
        last_db_update = st.session_state.coffee_purchase_db_update,
        time_frame = time_frame,
        max_items = max_items,
        producers = producers
    )

    coffee_bean_purchase_id = st.selectbox(
        "Coffee variety",
        options = coffee_dict,
        format_func = lambda x: coffee_dict[x], 
        index = None
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
                value = user_defaults["tamping_weight_kg"],
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

with st.container(border = True):
    st.header("Extraction parameters")

    col1, col2 = st.columns(2)

    with col1:

        grind_setting = st.number_input(
            "Grind setting",
            min_value = 0,
            max_value = 100, 
            value = 10,
            step = 1
        )

        dose_gr = st.number_input(
            "Coffee amount (gr)",
            min_value = 1.0,
            max_value = 50.0,
            value = 16.0,
            step = 0.1
        )

        st.write("**Extracted espresso yield (gr)**")
        yield_gr = st.number_input(
            "Please enter the yield",
            min_value = 1.0,
            max_value = 100.0,
            value = 30.0, 
            label_visibility = "collapsed", 
            step = 0.1
        )


    
    with col2:

        water_temp_c = st.number_input(
            "Water temperature (°C)",
            min_value = 50,
            max_value = 120,
            value = 93,
            step = 1
        )

        extraction_time_sec = st.number_input(
            "Extraction time (sec)",
            min_value = 1,
            max_value = 120,
            value = 25,
            step = 1
        )

        if dose_gr and yield_gr:
            st.write(
                f"""**Extraction ratio**:\n
                {round(yield_gr / dose_gr, 2)}"""
            )

payload = {
    "user_id" : st.session_state.current_user_id,
    "grinder_id" : grinder_id,
    "coffee_machine_id" : coffee_machine_id,
    "basket_pressurized" : basket_pressurized,
    "basket_shot_size" : basket_shot_size,
    "portafilter_spout" : portafilter_spout,
    "coffee_bean_purchase_id" : coffee_bean_purchase_id,
    "wdt_used" : wdt_used,
    "leveler_used" : leveler_used,
    "tamping_method" : tamping_method,
    "tamping_weight_kg" : tamping_weight_kg,
    "puck_screen_used" : puck_screen_used,
    "puck_screen_thickness_mm" : puck_screen_thickness_mm,
    "grind_setting" : grind_setting,
    "dose_gr" : dose_gr,
    "water_temp_c" : water_temp_c,
    "extraction_time_sec" : extraction_time_sec, 
    "yield_gr" : yield_gr
}

if st.button("Save espresso"):
    save_espresso_resp = requests.post(
        f"{st.session_state.backend_url}/new_espresso/save_espresso",
        json = payload
    )
    show_response_feedback(save_espresso_resp)
    if save_espresso_resp.status_code == 200:
        save_espresso_dict = save_espresso_resp.json()
        st.session_state.last_espresso_id = save_espresso_dict["id"]
        st.session_state.last_espresso_datetime = save_espresso_dict["experiment_datetime"]
    
if st.session_state.last_espresso_id:
    with st.form("eval_form", border = True):
        st.header("Evaluation")
        st.write(f"You can evaluate the espresso you saved at {st.session_state.last_espresso_datetime}.")
        evaluation_general = st.slider("Overall", 1, 10, 5)
        evaluation_flavor = st.slider("Flavor", 1, 10, 5)
        evaluation_body = st.slider("Body", 1, 10, 5)
        evaluation_crema = st.slider("Crema", 1, 10, 5)
        evaluation_notes = st.text_input("Comments and notes")
        eval_submit = st.form_submit_button("Save evaluation")
    if eval_submit:
        eval_espresso_resp = requests.patch(
            f"{st.session_state.backend_url}/new_espresso/save_espresso/evaluate",
            json = {
                "id" : st.session_state.last_espresso_id,
                "evaluation_general" : evaluation_general,
                "evaluation_flavor" : evaluation_flavor,
                "evaluation_body" : evaluation_body,
                "evaluation_crema" : evaluation_crema,
                "evaluation_notes" : evaluation_notes
            }
        )
        show_response_feedback(eval_espresso_resp)
    
