import streamlit as st
import requests

@st.cache_data
def get_user_list():
    user_dict_resp = requests.get(f"{st.session_state.backend_url}/users/")
    if user_dict_resp.status_code == 200:
        return user_dict_resp.json()
    else:
        st.error("Error fetching user data. Please try again later.")
        st.stop()

def return_if_200(response):
    if response.status_code == 200:
        return response.json()
    else:
        None

@st.cache_data
def get_user_defaults(user_id : int,
    last_db_update = st.session_state.default_setup_db_update) -> dict:
    user_defaults_resp = requests.get(
        f"{st.session_state.backend_url}/user_defaults/{user_id}"
    )
    return return_if_200(user_defaults_resp)

def find_default_index(lookup_iterable, defaults_dict : dict, look_for):    
    
    if defaults_dict is None:
        return None
    elif defaults_dict[look_for] is None:
        return None
    else:
        default_value = str(defaults_dict[look_for])

    if default_value not in lookup_iterable:
        return None
    
    if type(lookup_iterable) is list:
        options_list = lookup_iterable
    elif type(lookup_iterable) is dict:
        options_list = list(lookup_iterable.keys())
    else:
        return None
    
    return options_list.index(default_value)

@st.cache_data
def get_users_equipment_data(user_id : int, 
    last_db_update = st.session_state.equipment_owned_db_update) -> dict:
    equipment_data_resp = requests.get(
        f"{st.session_state.backend_url}/equipment/{user_id}"
    )
    return return_if_200(equipment_data_resp)

@st.cache_data
def get_users_coffee_producer_list(user_id : int, 
    last_db_update = st.session_state.coffee_purchase_db_update,
    time_frame : int = 30, max_items : int = 10) -> dict:
    producer_list_resp = requests.get(
        f"{st.session_state.backend_url}/coffee/producers/{user_id}", 
        params = {
            "time_frame" : time_frame,
            "max_items" : max_items
        }
    )
    return return_if_200(producer_list_resp)

@st.cache_data
def get_users_coffee_data(user_id : int, 
    last_db_update = st.session_state.coffee_purchase_db_update,
    time_frame : int = 30, max_items : int = 10, producers : list = None) -> dict:
    coffee_data_resp = requests.get(
        f"{st.session_state.backend_url}/coffee/purchases/{user_id}", 
        params = {
            "time_frame" : time_frame,
            "max_items" : max_items,
            "producers" : producers
        }
    )
    return return_if_200(coffee_data_resp)

def show_response_feedback(response):
    if response.status_code == 200:
        st.success(f"{response.json()['message']}")
    else:
        st.error("Something went wrong. Please try again.")

@st.cache_data
def get_all_coffee_varieties(producers : list = None,
    last_db_update = st.session_state.coffee_variety_db_update,
) -> dict:
    all_coffee_varieties_resp = requests.get(
        f"{st.session_state.backend_url}/coffee/all_varieties/", 
        params = {
            "producers" : producers
        }
    )
    return all_coffee_varieties_resp.json()

@st.cache_data
def get_all_producers_list(
    last_db_update = st.session_state.coffee_variety_db_update,
) -> dict:
    all_producers_resp = requests.get(
        f"{st.session_state.backend_url}/coffee/all_producers/"
    )
    return return_if_200(all_producers_resp)

@st.cache_data
def get_all_sellers_list(
    last_db_update = st.session_state.coffee_purchase_db_update,
) -> dict:
    all_sellers_resp = requests.get(
        f"{st.session_state.backend_url}/coffee/all_sellers/"
    )
    return return_if_200(all_sellers_resp)

@st.cache_data
def get_all_coffee_machines_dict(
    manufacturers : list = None,
    last_db_update = st.session_state.coffee_machine_db_update,
) -> dict:
    all_equipment_resp = requests.get(
        f"{st.session_state.backend_url}/equipment/coffee_machines/",
        params = {
            "manufacturers" : manufacturers
        }
    )
    return return_if_200(all_equipment_resp)

@st.cache_data
def get_all_coffee_machine_manufacturers_list(
    last_db_update = st.session_state.coffee_machine_db_update,
) -> dict:
    all_equipment_resp = requests.get(
        f"{st.session_state.backend_url}/equipment/coffee_machine_manufacturers/"
    )
    return return_if_200(all_equipment_resp)

@st.cache_data
def get_all_grinders_dict(
    manufacturers : list = None,
    last_db_update = st.session_state.grinder_db_update,
) -> dict:
    all_equipment_resp = requests.get(
        f"{st.session_state.backend_url}/equipment/grinders/", 
        params = {
            "manufacturers" : manufacturers
        }
    )
    return return_if_200(all_equipment_resp)

@st.cache_data
def get_all_grinder_manufacturers_list(
    last_db_update = st.session_state.grinder_db_update,
) -> dict:
    all_equipment_resp = requests.get(
        f"{st.session_state.backend_url}/equipment/grinder_manufacturers/"
    )
    return return_if_200(all_equipment_resp)

@st.cache_data
def get_equipment_sellers_list(
    last_db_update = st.session_state.equipment_owned_db_update,
) -> dict:
    all_equipment_resp = requests.get(
        f"{st.session_state.backend_url}/equipment/all_sellers/"
    )
    return return_if_200(all_equipment_resp)

@st.cache_data
def get_espresso_filter_default_range(user_id : int) -> dict:
    filter_default_range_resp = requests.get(
        f"{st.session_state.backend_url}/espresso_data/filter_default_range/{user_id}"
    )
    return return_if_200(filter_default_range_resp)

@st.cache_data
def get_coffee_dict_from_espresso(user_id : int) -> dict:
    coffee_dict_resp = requests.get(
        f"{st.session_state.backend_url}/espresso_data/coffee_list/{user_id}"
    )
    return return_if_200(coffee_dict_resp)

@st.cache_data
def get_machine_dict_from_espresso(user_id : int) -> dict:
    machine_dict_resp = requests.get(
        f"{st.session_state.backend_url}/espresso_data/machine_list/{user_id}"
    )
    return return_if_200(machine_dict_resp)

@st.cache_data
def get_grinder_dict_from_espresso(user_id : int) -> dict:
    grinder_dict_resp = requests.get(
        f"{st.session_state.backend_url}/espresso_data/grinder_list/{user_id}"
    )
    return return_if_200(grinder_dict_resp)