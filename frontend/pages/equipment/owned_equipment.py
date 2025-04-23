import streamlit as st
from src.helpers import (
    get_all_coffee_machines_dict,
    get_all_coffee_machine_manufacturers_list, 
    get_all_grinders_dict,
    get_all_grinder_manufacturers_list,
    get_all_portafilters_dict,
    get_all_portafilter_manufacturers_list, 
    get_equipment_sellers_list, 
    show_response_feedback
)
import requests
from datetime import datetime

st.title("Owned Equipment")
st.write("Add an equipment item to your owned equipment list.")

st.header("Equipment Type")

equipment_type_map = {
    "coffee machine": "Coffee Machine",
    "grinder": "Grinder",
    "portafilter": "Portafilter"
}

equipment_type = st.segmented_control(
    "Please select the type of equipment you want to add:",
    options = equipment_type_map,
    format_func = lambda x: equipment_type_map[x],
)

if equipment_type:
    st.header(f"Add {equipment_type_map[equipment_type]}")

coffee_machine_id = None
grinder_id = None
portafilter_id = None

if equipment_type == "coffee machine":
    with st.expander("Filter by manufacturer"):
        with st.form(key = "coffee_machine_manufacturer_filter"):
            all_manufacturers = get_all_coffee_machine_manufacturers_list(
                last_db_update = st.session_state.coffee_machine_db_update
            )["manufacturers"]
            selected_manufacturers = st.multiselect(
                "Select manufacturers to filter by:",
                options = all_manufacturers,
                default = all_manufacturers
            )
            submit_button = st.form_submit_button(label = "Apply filter")

    coffee_machine_dict = get_all_coffee_machines_dict(
        manufacturers = selected_manufacturers,
        last_db_update = st.session_state.coffee_machine_db_update
    )
    coffee_machine_id = st.selectbox(
        "Please select a coffee machine:",
        options = coffee_machine_dict,
        format_func = lambda x: coffee_machine_dict[x],
        index = None
    )

elif equipment_type == "grinder":
    with st.expander("Filter by manufacturer"):
        with st.form(key = "grinder_manufacturer_filter"):
            all_manufacturers = get_all_grinder_manufacturers_list(
                last_db_update = st.session_state.grinder_db_update
            )["manufacturers"]
            selected_manufacturers = st.multiselect(
                "Select manufacturers to filter by:",
                options = all_manufacturers,
                default = all_manufacturers
            )
            submit_button = st.form_submit_button(label = "Apply filter")
    
    grinder_dict = get_all_grinders_dict(
        manufacturers = selected_manufacturers,
        last_db_update = st.session_state.grinder_db_update
    )   
    grinder_id = st.selectbox(
        "Please select a grinder:",
        options = grinder_dict,
        format_func = lambda x: grinder_dict[x],
        index = None
    )

elif equipment_type == "portafilter":
    with st.expander("Filter by manufacturer"):
        with st.form(key = "portafilter_manufacturer_filter"):
            all_manufacturers = get_all_portafilter_manufacturers_list(
                last_db_update = st.session_state.portafilter_db_update
            )["manufacturers"]
            selected_manufacturers = st.multiselect(
                "Select manufacturers to filter by:",
                options = all_manufacturers,
                default = all_manufacturers
            )
            submit_button = st.form_submit_button(label = "Apply filter")
    
    portafilter_dict = get_all_portafilters_dict(
        manufacturers = selected_manufacturers,
        last_db_update = st.session_state.portafilter_db_update
    )
    portafilter_id = st.selectbox(
        "Please select a portafilter:",
        options = portafilter_dict,
        format_func = lambda x: portafilter_dict[x],
        index = None
    )

if coffee_machine_id or grinder_id or portafilter_id:
    st.header("Purchase details")
    
    st.subheader("Purchased from")
    left1, right1 = st.columns([0.67, 0.33], vertical_alignment = "bottom")

    equipment_sellers = get_equipment_sellers_list(
        last_db_update = st.session_state.equipment_owned_db_update
    )["sellers"]

    with right1:
        unknown_seller = st.toggle("Unknown seller")
        manual_seller = st.toggle("Seller not on the list", key = "enter_manually")
    
    with left1:
        if manual_seller:
            purchased_from = st.text_input(
                "Please enter the seller name",
                value = None
            )
        else:
            purchased_from = st.selectbox(
                "Please select a seller",
                options = equipment_sellers,
                index = None, 
                disabled = unknown_seller
            )
            if unknown_seller:
                purchased_from = None
 
    left2, right2 = st.columns(2)

    with left2:
        st.subheader("Purchase date")
        purchase_date = st.date_input(
            "Please select a date",
            value = None,
            min_value = None,
            max_value = None
        )

    with right2:
        st.subheader("Purchase price")
        purchase_price_eur = st.number_input(
            "Please enter the purchase price (EUR)",
            value = None,
            min_value = 0.0,
            max_value = None,
            step = 0.01
        )

    payload = {
        "user_id": st.session_state.current_user_id,
        "equipment_type": equipment_type,
        "coffee_machine_id": coffee_machine_id,
        "grinder_id": grinder_id,
        "portafilter_id": portafilter_id,
        "purchase_date": purchase_date,
        "purchased_from": purchased_from,
        "purchase_price_eur": purchase_price_eur
    }

    if st.button("Add item to owned equipment list"):
        add_equipment_resp = requests.post(
            f"{st.session_state.backend_url}/equipment/add_owned_equipment/",
            json = payload
        )
        show_response_feedback(add_equipment_resp)
        if add_equipment_resp.status_code == 200:
            st.session_state.equipment_owned_db_update = datetime.now()