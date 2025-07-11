import streamlit as st
from src.helpers import (
    get_espresso_filter_default_range
)

st.title("Explore Espresso Data")

st.header("Your own data or all users' data?")
own_or_all = st.segmented_control(
    "Please select",
    options = ["Your own data", "All users' data"]
)

if own_or_all is None:
    st.stop()

if own_or_all == "Your own data":
    user_id = st.session_state.current_user_id
else:
    user_id = 0

default_range_dict = get_espresso_filter_default_range(user_id)
st.write(default_range_dict)

with st.container(border = True):
    st.header("Filters")
    left1, right1 = st.columns([0.5, 0.5], vertical_alignment = "bottom")

    with left1:
        date_from = st.date_input(
            "Date from",
            value = default_range_dict["min_date"],
            help = "Select the start date of the data."
        )
    with right1:
        date_until = st.date_input(
            "Date until",
            value = default_range_dict["max_date"],
            help = "Select the end date of the data."
        )

    coffee_beans = st.multiselect(
        "Coffee beans",
        options = []
    )

    with st.expander("Equipment selection"):
        left2, right2 = st.columns([0.5, 0.5], vertical_alignment = "top")

        with left2:
            coffee_machine = st.multiselect(
                "Coffee machine",
                options = []
            )
            basket_pressurized = st.radio(
                "Pressurized basket",
                options = ["yes", "no"], 
                index = None
            )
            portafilter_spout = st.radio(
                "Portafilter spout type",
                options = ["single", "double", "bottomless"], 
                index = None
            )
            
        with right2:
            grinder = st.multiselect(
                "Grinder",
                options = []
            )
            basket_shot_size = st.radio(
                "Basket shot size",
                options = ["single", "double"], 
                index = None
            )
    
    with st.expander("Preparation methods"):
        left3, right3 = st.columns([0.5, 0.5], vertical_alignment = "bottom")

        with left3:
            wdt_used = st.radio(
                "WDT used",
                options = ["yes", "no"], 
                index = None
            )
            puck_screen_used = st.radio(
                "Puck screen used",
                options = ["yes", "no"], 
                index = None
            )
            
        with right3:
            tamping_method = st.radio(
                "Tamping method",
                options = ["manual", "automatic"], 
                index = None
            )
            leveler_used = st.radio(
                "Leveler used",
                options = ["yes", "no"], 
                index = None
            )
    
    with st.expander("Extraction parameters"):
        
        st.subheader("Grind level relative to the grinder's espresso range")
        grind_level_from, grind_level_to = st.select_slider(
            "Please select the range",
            key = "grind_level_slider",
            options = [round(i * 0.1, 1) for i in range(0, 51)],
            value = (
                default_range_dict["min_grind_level"], 
                default_range_dict["max_grind_level"]
            ),
            format_func = lambda x: f"{x:.1f}"
        )
        
        grinder_name = "Baratza Encore ESP"
        range_min = 0.0
        range_max = 20.0
        converted_min = int(grind_level_from * (range_max - range_min) + range_min)
        converted_max = int(grind_level_to * (range_max - range_min) + range_min)
        st.write(f"For grinder **{grinder_name}** the selected range is from **{converted_min}** to **{converted_max}**")

        st.subheader("Dose (gr)")
        dose_from, dose_to = st.select_slider(
            "Please select the range",
            key = "dose_slider",
            options = [round(i * 0.1, 1) for i in range(50, 301)],
            value = (
                float(default_range_dict["min_dose"]), 
                float(default_range_dict["max_dose"])
            )
        )
        left5, right5 = st.columns([0.5, 0.5], vertical_alignment = "bottom")

        st.subheader("Extraction time (seconds)")
        time_from, time_to = st.select_slider(
            "Please select the range",
            key = "time_slider",
            options = [i for i in range(5, 46)],
            value = (
                default_range_dict["min_time"], 
                default_range_dict["max_time"]
            ),
            format_func = lambda x: f"{x} sec"
        )

        st.subheader("Yield (gr)")
        yield_from, yield_to = st.select_slider(
            "Please select the range",
            key = "yield_slider",
            options = [round(i * 0.01, 1) for i in range(100, 10001)],
            value = (
                float(default_range_dict["min_yield"]), 
                float(default_range_dict["max_yield"])
            ),
            format_func = lambda x: f"{x:.2f}"
        )

        st.subheader("Extraction ratio")
        ratio_from, ratio_to = st.select_slider(
            "Please select the range",
            key = "ratio_slider",
            options = [round(i * 0.01, 2) for i in range(1, 501)],
            value = (
                float(default_range_dict["min_ratio"]), 
                float(default_range_dict["max_ratio"])
            ),
            format_func = lambda x: f"{x:.2f}"
        )

    with st.expander("Evaluation"):

        st.subheader("General evaluation")
        general_evaluation = st.select_slider(
            "Please select the range",
            key = "general_evaluation_slider",
            options = [i for i in range(1, 11)],
            value = (
                default_range_dict["min_evaluation_general"], 
                default_range_dict["max_evaluation_general"]
            )
        )

        st.subheader("Evaluation of flavor")
        flavor_evaluation = st.select_slider(
            "Please select the range",
            key = "flavor_evaluation_slider",
            options = [i for i in range(1, 11)],
            value = (
                default_range_dict["min_evaluation_flavor"], 
                default_range_dict["max_evaluation_flavor"]
            )
        )

        st.subheader("Evaluation of body")
        body_evaluation = st.select_slider(
            "Please select the range",
            key = "body_evaluation_slider",
            options = [i for i in range(1, 11)],
            value = (
                default_range_dict["min_evaluation_body"], 
                default_range_dict["max_evaluation_body"]
            )
        )

        st.subheader("Evaluation of crema")
        crema_evaluation = st.select_slider(
            "Please select the range",
            key = "crema_evaluation_slider",
            options = [i for i in range(1, 11)],
            value = (
                default_range_dict["min_evaluation_crema"], 
                default_range_dict["max_evaluation_crema"]
            )
        )


