import streamlit as st
import requests
from src.helpers import get_user_list

user_dict = get_user_list()

st.title("Home")

if not st.session_state.logged_in:
    st.header("Check in")
    st.write("Please check in to access the app.")

    select_user = st.selectbox(
        "Type or select your user name", 
        user_dict, 
        format_func = lambda x: user_dict[x]
    )

    if select_user and st.button("Check in"):
        current_user_id = select_user
        user_checkin_resp = requests.post(
            f"http://localhost:8000/users/{current_user_id}"
        )
        if user_checkin_resp.status_code == 200:
            st.session_state.current_user_id = current_user_id
            st.session_state.current_user_name = user_dict[current_user_id]
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Error checking in. Please try again.")
    

if st.session_state.logged_in:
    st.header("Welcome back!")
    st.write(f"You are now checked in as **{st.session_state.current_user_name}**.")
    st.write("If you want to check out, click the botton below.")

    if st.button("Check out"):
        user_checkout_resp = requests.post(
            "http://localhost:8000/users/0"
        )
        if user_checkout_resp.status_code == 200:
            st.session_state.current_user_id = None
            st.session_state.current_user_name = None
            st.session_state.logged_in = False
            st.rerun()
        else:
            st.error("Error checking out. Please try again.")