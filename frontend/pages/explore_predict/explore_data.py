import streamlit as st
from src.helpers import (
    get_espresso_filter_default_range, 
    get_coffee_dict_from_espresso, 
    get_machine_dict_from_espresso, 
    get_grinder_dict_from_espresso
)

st.title("Explore Espresso Data")

st.header("Data selection")
own_or_all = st.segmented_control(
    "Would you like to explore your own data or all users' data?",
    options = ["Your own data", "All users' data"]
)

if own_or_all is None:
    st.stop()
if own_or_all == "Your own data":
    user_id = st.session_state.current_user_id
else:
    user_id = 0

apply_filters = st.toggle("Apply filters?")

if apply_filters:

    default_range_dict = get_espresso_filter_default_range(user_id)
    default_coffee_dict = get_coffee_dict_from_espresso(user_id)
    default_machine_dict = get_machine_dict_from_espresso(user_id)
    default_grinder_dict = get_grinder_dict_from_espresso(user_id)

    with st.container(border = True):
        st.header("Filters")

        with st.expander("Dates"):
            left1, right1 = st.columns([0.5, 0.5])
            with left1:
                date_from = st.date_input(
                    "From",
                    value = default_range_dict["min_date"],
                    min_value = default_range_dict["min_date"],
                    max_value = default_range_dict["max_date"],
                    help = "Select the start date of the data."
                )
            with right1:
                date_until = st.date_input(
                    "Until",
                    value = default_range_dict["max_date"],
                    min_value = default_range_dict["min_date"],
                    max_value = default_range_dict["max_date"],
                    help = "Select the end date of the data."
                )

        with st.expander("Coffee selection"):
            coffee_beans = st.multiselect(
                "Coffee beans",
                options = default_coffee_dict, 
                default = default_coffee_dict, 
                format_func = lambda x: default_coffee_dict[x]
            )

        with st.expander("Equipment selection"):
            left2, right2 = st.columns([0.5, 0.5])
            with left2:
                coffee_machine = st.multiselect(
                    "Coffee machine",
                    options = default_machine_dict, 
                    default = default_machine_dict, 
                    format_func = lambda x: default_machine_dict[x]
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
                    options = default_grinder_dict, 
                    default = default_grinder_dict, 
                    format_func = lambda x: default_grinder_dict[x][0]
                )
                basket_shot_size = st.radio(
                    "Basket shot size",
                    options = ["single", "double"], 
                    index = None
                )

        with st.expander("Preparation methods"):
            left3, right3 = st.columns([0.5, 0.5])
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
                options = [round(i * 0.1, 1) for i in range(
                    default_range_dict["min_grind_level"]*10, 
                    default_range_dict["max_grind_level"]*10+1
                )],
                value = (
                    default_range_dict["min_grind_level"], 
                    default_range_dict["max_grind_level"]
                ),
                format_func = lambda x: f"{x:.1f}"
            )
            
            for g in default_grinder_dict:
                grinder_name = default_grinder_dict[g][0]
                range_min = default_grinder_dict[g][1]
                range_max = default_grinder_dict[g][2]
                converted_min = int(grind_level_from * (range_max - range_min) + range_min)
                converted_max = int(grind_level_to * (range_max - range_min) + range_min)
                st.write(f"For grinder **{grinder_name}** the selected range is from **{converted_min}** to **{converted_max}**")

            st.subheader("Dose (gr)")
            dose_from, dose_to = st.select_slider(
                "Please select the range",
                key = "dose_slider",
                options = [round(i * 0.1, 1) for i in range(
                    int(float(default_range_dict["min_dose"])*10), 
                    int(float(default_range_dict["max_dose"])*10+1)
                    )],
                value = (
                    float(default_range_dict["min_dose"]), 
                    float(default_range_dict["max_dose"])
                )
            )

            st.subheader("Extraction time (seconds)")
            time_from, time_to = st.select_slider(
                "Please select the range",
                key = "time_slider",
                options = [i for i in range(
                    default_range_dict["min_time"], 
                    default_range_dict["max_time"]+1
                    )],
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
                options = [round(i * 0.1, 1) for i in range(
                    int(float(default_range_dict["min_yield"])*10), 
                    int(float(default_range_dict["max_yield"])*10+1)
                    )],
                value = (
                    float(default_range_dict["min_yield"]), 
                    float(default_range_dict["max_yield"])
                )
            )

            st.subheader("Extraction ratio")
            ratio_from, ratio_to = st.select_slider(
                "Please select the range",
                key = "ratio_slider",
                options = [round(i * 0.01, 2) for i in range(
                    int(float(default_range_dict["min_ratio"])*100), 
                    int(float(default_range_dict["max_ratio"])*100+1)
                    )],
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


