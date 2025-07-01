import streamlit as st

def init_session_state_vars():
    if "backend_url" not in st.session_state:
        st.session_state.backend_url = None
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user_id" not in st.session_state:
        st.session_state.current_user_id = None
    if "current_user_name" not in st.session_state:
        st.session_state.current_user_name = None
    if "last_espresso_id" not in st.session_state:
        st.session_state.last_espresso_id = None
    if "last_espresso_datetime" not in st.session_state:
        st.session_state.last_espresso_datetime = None
    if "default_setup_db_update" not in st.session_state:
        st.session_state.default_setup_db_update = None
    if "coffee_machine_db_update" not in st.session_state:
        st.session_state.coffee_machine_db_update = None
    if "grinder_db_update" not in st.session_state:
        st.session_state.grinder_db_update = None
    if "equipment_owned_db_update" not in st.session_state:
        st.session_state.equipment_owned_db_update = None
    if "coffee_variety_db_update" not in st.session_state:
        st.session_state.coffee_variety_db_update = None
    if "coffee_purchase_db_update" not in st.session_state:
        st.session_state.coffee_purchase_db_update = None