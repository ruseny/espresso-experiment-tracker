import streamlit as st
from src.session_state_vars import init_session_state_vars

init_session_state_vars()

import os
from dotenv import load_dotenv
load_dotenv()
backend_host = os.getenv("BACKEND_HOST")
backend_port = os.getenv("BACKEND_PORT")
backend_url = f"http://{backend_host}:{backend_port}"
st.session_state.backend_url = backend_url

home_page = st.Page (
    "pages/home.py", 
    title = "Home", 
    default = True, 
    icon = ":material/home:"
)

new_espresso = st.Page(
    "pages/espresso/new_espresso.py", 
    title = "New Espresso", 
    icon = ":material/coffee:"
)

default_setup = st.Page(
    "pages/inventory/default_setup.py", 
    title = "Default Setup", 
    icon = ":material/settings:"
)

coffee_purchase = st.Page(
    "pages/inventory/coffee_purchase.py", 
    title = "Coffee Purchases", 
    icon = ":material/shopping_bag:"
)

new_coffee_variety = st.Page(
    "pages/selection/new_coffee_variety.py", 
    title = "Add Coffee Variety", 
    icon = ":material/shopping_bag:"
)

owned_equipment = st.Page(
    "pages/selection/owned_equipment.py",
    title = "Equipment Purchases",
    icon = ":material/coffee_maker:"
)

new_equipment = st.Page(
    "pages/inventory/new_equipment.py",
    title = "Add Equipment",
    icon = ":material/coffee_maker:"
)

explore_espresso_data = st.Page(
    "pages/espresso/explore_data.py",
    title = "Explore Espresso Data",
    icon = ":material/search:"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

if st.session_state.logged_in:
    entry = st.navigation(
        {
            "Home" : [home_page], 
            "Espresso" : [new_espresso, explore_espresso_data], 
            "Inventory" : [coffee_purchase, owned_equipment, default_setup],
            "Selection" : [new_coffee_variety, new_equipment]
        }
    )
else:
    entry = st.navigation([home_page])

entry.run()