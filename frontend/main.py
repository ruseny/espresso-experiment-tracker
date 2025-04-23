import streamlit as st
from src.session_state_vars import init_session_state_vars

init_session_state_vars()

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
    "pages/espresso/default_setup.py", 
    title = "Default Setup", 
    icon = ":material/settings:"
)

coffee_purchase = st.Page(
    "pages/coffee_beans/coffee_purchase.py", 
    title = "Coffee Purchase", 
    icon = ":material/shopping_bag:"
)

new_coffee_variety = st.Page(
    "pages/coffee_beans/new_coffee_variety.py", 
    title = "New Coffee Variety", 
    icon = ":material/add_circle:"
)

owned_equipment = st.Page(
    "pages/equipment/owned_equipment.py",
    title = "Owned Equipment",
    icon = ":material/coffee_maker:"
)

new_equipment = st.Page(
    "pages/equipment/new_equipment.py",
    title = "New Equipment",
    icon = ":material/add_circle:"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

if st.session_state.logged_in:
    entry = st.navigation(
        {
            "Home" : [home_page], 
            "Making Espresso" : [new_espresso, default_setup], 
            "Coffee Beans" : [coffee_purchase, new_coffee_variety], 
            "Equipment" : [owned_equipment, new_equipment]
        }
    )
else:
    entry = st.navigation([home_page])

entry.run()