import streamlit as st
from src.helpers import (
    get_all_producers_list, 
    show_response_feedback
)
import requests
from datetime import datetime

st.title("Add new coffee variety")

st.header("Details of new coffee variety")

left1, right1 = st.columns(2)

with left1:
    st.subheader("Producer")

    producers_list = get_all_producers_list(
        last_db_update = st.session_state.coffee_variety_db_update
    )["producers_list"]

    if st.toggle("Producer not in the list?"):
        producer = st.text_input(
            "Please enter new producer name"
        )
    else:
        producer = st.selectbox(
            "Please select the producer",
            options = producers_list
        )
with right1:
    st.subheader("Coffee variety name")

    name = st.text_input(
        "Please enter the coffee variety name"
    )

left2, right2 = st.columns(2)

with left2:
    st.subheader("Origin")

    origin = st.text_input(
        "Please enter the coffee variety origin"
    )

with right2:
    st.subheader("Origin type")

    origin_type_map = {
        "single_origin" : "single origin", 
        "blend" : "blend"
    }
    origin_type = st.radio(
        "Please select origin type", 
        options = origin_type_map,
        format_func = lambda x: origin_type_map[x]
    )

left3, right3 = st.columns(2, vertical_alignment = "bottom")
with left3:
    st.subheader("Arabica ratio")
    arabica_ratio_map = {
        1.0 : "100% arabica",
        0.8 : "80% arabica",
        0.7 : "70% arabica", 
        "other" : "Other percentage"
    }
    arabica_unknown = st.toggle("Arabica ratio unknown?")
    arabica_ratio_radio = st.radio(
        "Please select the arabica ratio...",
        options = arabica_ratio_map,
        format_func = lambda x: arabica_ratio_map[x],
        index = None,
        disabled = arabica_unknown
    )
    arabica_radio_selected = arabica_ratio_radio in [1.0, 0.8, 0.7]

with right3:
    arabica_perc_slider = st.slider(
        "... or use the slider.",
        min_value = 0,
        max_value = 100,
        value = None,
        step = 1,
        disabled = arabica_unknown or arabica_radio_selected
    )

if arabica_unknown:
    arabica_ratio = None
elif arabica_radio_selected:
    arabica_ratio = arabica_ratio_radio
else:
    arabica_ratio = arabica_perc_slider / 100

st.subheader("Coffee profile ratings")

margin4, left4, centre4, right4 = st.columns(
    [0.2, 0.39, 0.02, 0.39], vertical_alignment = "bottom"
)
with margin4:
    st.write("**Roast level**")
    roast_level_unknown = st.toggle("Unknown?", key = "roast_level_unknown")
with left4:
    roast_level_val = st.number_input(
        "Roast level rating",
        min_value = 0,
        max_value = 10,
        value = 4,
        step = 1,
        disabled = roast_level_unknown
    )
with centre4:
    st.write("/")
with right4:
    roast_level_scale = st.number_input(
        "Roast level scale",
        min_value = 2,
        max_value = 10,
        value = 5, 
        step = 1,
        disabled = roast_level_unknown
    )
if roast_level_unknown:
    roast_level = None
else: 
    roast_level = roast_level_val / roast_level_scale

margin5, left5, centre5, right5 = st.columns(
    [0.2, 0.39, 0.02, 0.39], vertical_alignment = "bottom"
)
with margin5:
    st.write("**Intensity**")
    intensity_unknown = st.toggle("Unknown?", key = "intensity_unknown")
with left5:
    intensity_val = st.number_input(
        "Intensity rating",
        min_value = 0,
        max_value = 10,
        value = 4, 
        step = 1, 
        disabled = intensity_unknown
    )
with centre5:
    st.write("/")
with right5:
    intensity_scale = st.number_input(
        "Intensity scale",
        min_value = 2,
        max_value = 10,
        value = 5, 
        step = 1, 
        disabled = intensity_unknown
    )
if intensity_unknown:
    intensity = None
else:
    intensity = intensity_val / intensity_scale

margin6, left6, centre6, right6 = st.columns(
    [0.2, 0.39, 0.02, 0.39], vertical_alignment = "bottom"
)
with margin6:
    st.write("**Acidity**")
    acidity_unknown = st.toggle("Unknown?", key = "acidity_unknown")
with left6:
    acidity_val = st.number_input(
        "Acidity rating",
        min_value = 0,
        max_value = 10,
        value = 1, 
        step = 1, 
        disabled = acidity_unknown
    )
with centre6:
    st.write("/")
with right6:
    acidity_scale = st.number_input(
        "Acidity scale",
        min_value = 2,
        max_value = 10,
        value = 5,
        step = 1, 
        disabled = acidity_unknown
    )
if acidity_unknown:
    acidity = None
else:
    acidity = acidity_val / acidity_scale

left7, right7 = st.columns([0.6, 0.4])
with left7:
    st.subheader("Flavour notes")
    flavor_notes_list = st.pills(
        "Please select flavour notes",
        options = [
            "caramel", "brown sugar", "vanilla", 
            "chocolate", "nutty", "floral", "herbal",
            "fruity", "berry", "citrus", 
            "spice", "cinnamon", "nutmeg",  
            "earthy", "smoky", "tobacco", "oak"
        ],
        selection_mode = "multi", 
        default = None
    )
    flavor_notes_text = None
    if st.toggle("Additional notes?"):
        flavor_notes_text = st.text_input(
            "Please enter additional flavour notes:"
        )

flavor_notes = ", ".join(str(x) for x in flavor_notes_list)
if flavor_notes_text:
    flavor_notes += ", " + flavor_notes_text

with right7: 
    st.subheader("Decaf")
    decaffeinated = st.radio(
        "Is this decaffeinated?",
        options = ["yes", "no"], 
        index = 1
    )

payload = {
    "producer" : producer, 
    "name" : name, 
    "origin" : origin, 
    "origin_type" : origin_type, 
    "arabica_ratio" : arabica_ratio, 
    "roast_level" : roast_level, 
    "intensity" : intensity, 
    "acidity" : acidity, 
    "flavor_notes" : flavor_notes, 
    "decaffeinated" : decaffeinated
}

if st.button("Save new coffee variety"):
    new_coffe_variety_resp = requests.post(
        f"{st.session_state.backend_url}/coffee/varieties/save_new/",
        json = payload
    )
    show_response_feedback(new_coffe_variety_resp)
    if new_coffe_variety_resp.status_code == 200:
        st.session_state.coffee_variety_db_update = datetime.now()





