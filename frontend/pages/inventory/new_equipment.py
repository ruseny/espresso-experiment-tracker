import streamlit as st
from frontend.src.api_requests import (
    get_all_coffee_machine_manufacturers_list, 
    get_all_grinder_manufacturers_list,
    show_response_feedback
)
import requests
from datetime import datetime

st.title("New Equipment")
st.write("You can add new equipment here.")

st.header("Equipment type")

equipment_type_map = {
    "coffee machine": "Coffee Machine",
    "grinder": "Grinder"
}

equipment_type = st.segmented_control(
    "Please select the type of equipment you want to add:",
    options = equipment_type_map,
    format_func = lambda x: equipment_type_map[x],
)

if equipment_type is None:
    st.stop()

st.header(f"Add new {equipment_type_map[equipment_type]}")

st.subheader("Manufacturer")

if equipment_type == "coffee machine":
    all_manufacturers = get_all_coffee_machine_manufacturers_list(
        last_db_update = st.session_state.coffee_machine_db_update
    )["manufacturers"]
if equipment_type == "grinder":
    all_manufacturers = get_all_grinder_manufacturers_list(
        last_db_update = st.session_state.grinder_db_update
    )["manufacturers"]

left1, right1 = st.columns([0.67, 0.33], vertical_alignment = "bottom")

with right1:
    manual_manufacturer = st.toggle("Manufacturer not in the list")
with left1:
    if manual_manufacturer:
        manufacturer = st.text_input(
            "Please enter the manufacturer name:",
            value = None
        )
    else:
        manufacturer = st.selectbox(
            "Please select a manufacturer:",
            options = all_manufacturers,
            index = None
        )

if manufacturer is None:
    st.error("Manufacturer should be selected to entered to continue.")
    st.stop()

left2, right2 = st.columns(2)

with left2:
    st.subheader("Series")
    model_part_1 = st.text_input(
        "Please enter the series name:",
        value = None
    )
with right2:
    st.subheader("Model")
    model_part_2 = st.text_input(
        "Please enter the model name:",
        value = None
    )

if model_part_1 and model_part_2:
    model_name = model_part_1
    model_name_add = model_part_2
elif model_part_1:
    model_name = model_part_1
    model_name_add = None
elif model_part_2:
    model_name = model_part_2
    model_name_add = None
else:
    st.error(
        """At least one of the two fields, Series or Model, 
        should be filled in to continue."""
    )
    st.stop()

left3, right3 = st.columns(2)

with left3:
    st.subheader("Product identifier")
    product_identifier = st.text_input(
        "Please enter the manufacturer's number, EAN, etc.:",
        value = None
    )
    if product_identifier is None:
        product_identifier = "Not specified"

with right3:
    st.subheader("Specification")
    model_specification = st.text_input(
        "Please enter further details such as colour, material, etc.",
        value = None
    )


if equipment_type == "coffee machine":

    left4, right4 = st.columns(2)
    with left4:
        st.subheader("Pump pressure")
        pump_pressure_bar = st.number_input(
            "Please enter the pump pressure in bar:",
            min_value = 5,
            max_value = 25,
            value = None
        )
    with right4:
        st.subheader("Pump type")
        pump_type = st.text_input(
            "Please enter the pump type (e.g. rotary, vibratory):",
            value = None
        )

    left5, right5 = st.columns(2)
    with left5:
        st.subheader("Water temperature control")
        water_temp_control = st.text_input(
            "Please enter the water temperature control type (e.g. PID, manual):",
            value = None
        )
    with right5:
        st.subheader("PID control")
        pid_control = st.radio(
            "Please select the PID control type:",
            options = ["none", "automatic", "programmable"],
            index = 0
        )
    if pid_control == "none" or pid_control is None:
        pid_control = ""
    
    left6, right6 = st.columns(2)
    with left6:
        st.subheader("Boiler type")
        boiler_type = st.text_input(
            "Please enter the boiler type (e.g. double, heat exchange):",
            value = None
        )
    with right6:
        st.subheader("Portafilter diameter")
        portafilter_diam_mm = st.number_input(
            "Please enter the portafilter diameter in mm:",
            min_value = 45,
            max_value = 65,
            value = 58,
            step = 1
        )

if equipment_type == "grinder":

    left4, right4 = st.columns(2)
    with left4:
        st.subheader("Operation type")
        operation_type = st.radio(
            "Please select the operation type:",
            options = ["electric", "manual"],
            index = 0
        )
    with right4:
        st.subheader("Burr shape")
        burr_shape = st.text_input(
            "Please enter the burr shape (e.g. flat, conical):",
            value = None
        )

    left5, right5 = st.columns(2)
    with left5:
        st.subheader("Burr diameter")
        burr_diameter_mm = st.number_input(
            "Please enter the burr diameter in mm:",
            min_value = 30,
            max_value = 100,
            value = None
        )
    with right5:
        st.subheader("Burr material")
        burr_material = st.text_input(
            "Please enter the burr material (e.g. steel, ceramic):",
            value = None
        )

    st.subheader("Grinding levels")
    no_grinding_settings = st.toggle(
        "No consistent grinding settings",
        help = """This could be the case, for instance, 
        if the grinder has stepless adjustments, or
        the values can be rotated multiple times."""
    )
    if no_grinding_settings:
        min_setting = None
        max_setting = None
        min_espresso_range = None
        max_espresso_range = None
    else:
        left6, right6 = st.columns(2)
        with left6:
            st.write("Minimum setting")
            min_setting = st.number_input(
                "Please enter the minimum setting:",
                min_value = -20,
                max_value = 1,
                value = 0
            )
        with right6:
            st.write("Maximum setting")
            max_setting = st.number_input(
                "Please enter the maximum fine setting:",
                min_value = 5,
                max_value = 100,
                value = 20
            )

        st.write("Espresso range")
        left7, right7 = st.columns([0.75, 0.25], vertical_alignment = "center")
        with right7:
            esp_range_na = st.toggle("Not applicable?")
        with left7:
            min_espresso_range , max_espresso_range = st.select_slider(
                "Please select the espresso range:",
                options = range(min_setting, max_setting + 1),
                value = (min_setting, max_setting/2), 
                disabled = esp_range_na
            )
            if esp_range_na:
                min_espresso_range = None
                max_espresso_range = None

    left8, right8 = st.columns(2)
    with left8:
        st.subheader("Single dose")
        single_dose_used = st.radio(
            "Does the grinder use a single dose hopper?",
            options = ["yes", "no"],
            index = 1
        )

if st.button("Save new equipment"):

    if equipment_type == "coffee machine":
        payload = {
            "manufacturer": manufacturer,
            "model_name": model_name,
            "model_name_add": model_name_add,
            "model_specification": model_specification,
            "product_identifier": product_identifier,
            "pump_pressure_bar": pump_pressure_bar,
            "pump_type": pump_type,
            "water_temp_control": water_temp_control,
            "pid_control": pid_control,
            "boiler_type": boiler_type,
            "portafilter_diam_mm": portafilter_diam_mm
        }
        endpoint = "equipment/save_new_coffee_machine/"

    if equipment_type == "grinder":
        payload = {
            "manufacturer": manufacturer,
            "model_name": model_name,
            "model_name_add": model_name_add,
            "model_specification": model_specification,
            "product_identifier": product_identifier,
            "operation_type": operation_type,
            "burr_shape": burr_shape,
            "burr_diameter_mm": burr_diameter_mm,
            "burr_material": burr_material,
            "min_setting": min_setting,
            "max_setting": max_setting,
            "min_espresso_range": min_espresso_range,
            "max_espresso_range": max_espresso_range,
            "single_dose": single_dose_used
        }
        endpoint = "equipment/save_new_grinder/"

    new_equipment_resp = requests.post(
        f"{st.session_state.backend_url}/{endpoint}",
        json = payload
    )
    show_response_feedback(new_equipment_resp)
    if new_equipment_resp.status_code == 200:
        if equipment_type == "coffee machine":
            st.session_state.coffee_machine_db_update = datetime.now()
        if equipment_type == "grinder":
            st.session_state.grinder_db_update = datetime.now()

    



