import streamlit as st
from src.helpers import (
    get_all_coffee_varieties, 
    get_all_sellers_list, 
    show_response_feedback, 
    get_all_producers_list
)
from datetime import date, datetime, timedelta
import requests

st.title("Coffee Purchase")

st.header("Details of new coffee purchase")



sellers_list = get_all_sellers_list(
    last_db_update = st.session_state.coffee_purchase_db_update
)["sellers_list"]

left1, right1 = st.columns([0.65, 0.35], vertical_alignment = "bottom")

with left1:

    st.subheader("Coffee variety")

    with st.expander("Filter by producer"):

        producers_list = get_all_producers_list(
            last_db_update = st.session_state.coffee_variety_db_update
        )["producers_list"]

        with st.form("producer_filter_form"):
            producers = st.multiselect(
                "Please select", 
                options = producers_list,
                default = producers_list
            )
            st.form_submit_button("Apply filter")
        
    coffee_dict = get_all_coffee_varieties(
        producers = producers,
        last_db_update = st.session_state.coffee_variety_db_update
    )

    variety_id = st.selectbox(
        "Please select coffee variety",
        options = coffee_dict,
        format_func = lambda x: coffee_dict[x]
    )

with right1:
    if st.toggle("Coffee variety not in the list?"):
        if st.button("Add new coffee variety"):
            st.switch_page("pages/coffee_beans/new_coffee_variety.py")




left2, right2 = st.columns(2, vertical_alignment = "bottom")

with left2:
    st.subheader("Purchase date")
    today = st.toggle("Today")
    if today:
        default_date = date.today()
    else:
        default_date = date.today() - timedelta(days = 7)
    purchase_date = st.date_input(
        "Please select a date",
        value = default_date,
        min_value = date.today() - timedelta(days = 90),
        max_value = date.today(), 
        disabled = today
    )
st.write("Selected date : ", purchase_date)
    
with right2:
    st.subheader("Purchased from")
    if st.toggle("New retailer?"):
        purchased_from = st.text_input("Enter new retailer name")
    else:
        purchased_from = st.selectbox(
            "Please select retailer",
            options = sellers_list
        )

left3, right3 = st.columns(2)

with left3:
    st.subheader("Weight")
    weight_kg = st.number_input(
        "Please enter the weight (kg)",
        min_value = 0.05,
        max_value = 100.0,
        value = 0.25,
        step = 0.05
    )

with right3:
    st.subheader("Price")
    price = st.number_input(
        "Please enter the full price of the purchase (EUR)",
        min_value = 0.01,
        max_value = 1000.0,
        value = 10.0,
        step = 0.01
    )

price_per_kg_eur = price / weight_kg

left4, right4 = st.columns(2)

with left4:
    st.subheader("Roast date")
    if st.toggle("Date not known?"):
        roast_date = None
    else:
        roast_date = st.date_input(
            "Please select a date",
            value = purchase_date - timedelta(days = 7),
            min_value = purchase_date - timedelta(days = 720),
            max_value = purchase_date
        )

payload = {
    "user_id" : st.session_state.current_user_id,
    "variety_id" : variety_id,
    "purchase_date" : purchase_date.strftime("%Y-%m-%d"),
    "purchased_from" : purchased_from,
    "roast_date" : roast_date.strftime("%Y-%m-%d") if roast_date else None,
    "weight_kg" : weight_kg,
    "price_per_kg_eur" : price_per_kg_eur
}

if st.button("Save new purchase"):
    new_coffee_purchase_resp = requests.post(
        "http://localhost:8000/coffee/purchases/save_new/",
        json = payload
    )
    show_response_feedback(new_coffee_purchase_resp)
    if new_coffee_purchase_resp.status_code == 200:
        st.session_state.coffee_purchase_db_update = datetime.now()
