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

        def mark_changed_filter(name):
            st.session_state.espresso_data_applied_filters[name] = True

        with st.expander("Dates"):
            left1, right1 = st.columns([0.5, 0.5])
            with left1:
                date_from = st.date_input(
                    "From",
                    value = default_range_dict["min_date"],
                    min_value = default_range_dict["min_date"],
                    max_value = default_range_dict["max_date"],
                    help = "Select the start date of the data.", 
                    on_change = mark_changed_filter, 
                    kwargs = {"name": "date_from"}
                )
            with right1:
                date_until = st.date_input(
                    "Until",
                    value = default_range_dict["max_date"],
                    min_value = default_range_dict["min_date"],
                    max_value = default_range_dict["max_date"],
                    help = "Select the end date of the data.", 
                    on_change = mark_changed_filter, 
                    kwargs = {"name": "date_until"}
                )

        with st.expander("Coffee selection"):
            coffee_beans = st.multiselect(
                "Coffee beans",
                options = default_coffee_dict, 
                default = default_coffee_dict, 
                format_func = lambda x: default_coffee_dict[x], 
                on_change = mark_changed_filter,
                kwargs = {"name": "coffee_beans"}
            )

        with st.expander("Equipment selection"):
            left2, right2 = st.columns([0.5, 0.5])
            with left2:
                coffee_machine = st.multiselect(
                    "Coffee machine",
                    options = default_machine_dict, 
                    default = default_machine_dict, 
                    format_func = lambda x: default_machine_dict[x], 
                    on_change = mark_changed_filter,
                    kwargs = {"name": "coffee_machine"}
                )
                basket_pressurized = st.radio(
                    "Pressurized basket",
                    options = ["yes", "no"], 
                    index = None, 
                    on_change = mark_changed_filter,
                    kwargs = {"name": "basket_pressurized"}
                )
                portafilter_spout = st.radio(
                    "Portafilter spout type",
                    options = ["single", "double", "bottomless"], 
                    index = None, 
                    on_change = mark_changed_filter,
                    kwargs = {"name": "portafilter_spout"}
                )        
            with right2:
                grinder = st.multiselect(
                    "Grinder",
                    options = default_grinder_dict, 
                    default = default_grinder_dict, 
                    format_func = lambda x: default_grinder_dict[x][0], 
                    on_change = mark_changed_filter,
                    kwargs = {"name": "grinder"}
                )
                basket_shot_size = st.radio(
                    "Basket shot size",
                    options = ["single", "double"], 
                    index = None, 
                    on_change = mark_changed_filter,
                    kwargs = {"name": "basket_shot_size"}
                )

        with st.expander("Preparation methods"):
            left3, right3 = st.columns([0.5, 0.5])
            with left3:
                wdt_used = st.radio(
                    "WDT used",
                    options = ["yes", "no"], 
                    index = None, 
                    on_change = mark_changed_filter,
                    kwargs = {"name": "wdt_used"}
                )
                puck_screen_used = st.radio(
                    "Puck screen used",
                    options = ["yes", "no"], 
                    index = None, 
                    on_change = mark_changed_filter,
                    kwargs = {"name": "puck_screen_used"}
                )       
            with right3:
                tamping_method = st.radio(
                    "Tamping method",
                    options = ["manual", "automatic"], 
                    index = None, 
                    on_change = mark_changed_filter,
                    kwargs = {"name": "tamping_method"}
                )
                leveler_used = st.radio(
                    "Leveler used",
                    options = ["yes", "no"], 
                    index = None, 
                    on_change = mark_changed_filter,
                    kwargs = {"name": "leveler_used"}
                )
        
        with st.expander("Extraction parameters"):

            st.subheader("Grind level relative to the grinder's espresso range")
            grind_level = st.select_slider(
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
                format_func = lambda x: f"{x:.1f}", 
                on_change = mark_changed_filter,
                kwargs = {"name": "grind_level"}
            )
            
            for g in default_grinder_dict:
                grinder_name = default_grinder_dict[g][0]
                range_min = default_grinder_dict[g][1]
                range_max = default_grinder_dict[g][2]
                converted_min = int(grind_level[0] * (range_max - range_min) + range_min)
                converted_max = int(grind_level[1] * (range_max - range_min) + range_min)
                st.write(f"For grinder **{grinder_name}** the selected range is from **{converted_min}** to **{converted_max}**")

            st.subheader("Dose (gr)")
            dose_gr = st.select_slider(
                "Please select the range",
                key = "dose_slider",
                options = [round(i * 0.1, 1) for i in range(
                    int(float(default_range_dict["min_dose"])*10), 
                    int(float(default_range_dict["max_dose"])*10+1)
                    )],
                value = (
                    float(default_range_dict["min_dose"]), 
                    float(default_range_dict["max_dose"])
                ), 
                on_change = mark_changed_filter,
                kwargs = {"name": "dose_gr"}
            )

            st.subheader("Extraction time (seconds)")
            extr_time = st.select_slider(
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
                format_func = lambda x: f"{x} sec", 
                on_change = mark_changed_filter,
                kwargs = {"name": "extr_time"}
            )

            st.subheader("Yield (gr)")
            yield_gr = st.select_slider(
                "Please select the range",
                key = "yield_slider",
                options = [round(i * 0.1, 1) for i in range(
                    int(float(default_range_dict["min_yield"])*10), 
                    int(float(default_range_dict["max_yield"])*10+1)
                    )],
                value = (
                    float(default_range_dict["min_yield"]), 
                    float(default_range_dict["max_yield"])
                ), 
                on_change = mark_changed_filter,
                kwargs = {"name": "yield_gr"}
            )

            st.subheader("Extraction ratio")
            extr_ratio = st.select_slider(
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
                format_func = lambda x: f"{x:.2f}", 
                on_change = mark_changed_filter,
                kwargs = {"name": "extr_ratio"}
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
                ), 
                on_change = mark_changed_filter,
                kwargs = {"name": "general_evaluation"}
            )

            st.subheader("Evaluation of flavor")
            flavor_evaluation = st.select_slider(
                "Please select the range",
                key = "flavor_evaluation_slider",
                options = [i for i in range(1, 11)],
                value = (
                    default_range_dict["min_evaluation_flavor"], 
                    default_range_dict["max_evaluation_flavor"]
                ), 
                on_change = mark_changed_filter,
                kwargs = {"name": "flavor_evaluation"}
            )

            st.subheader("Evaluation of body")
            body_evaluation = st.select_slider(
                "Please select the range",
                key = "body_evaluation_slider",
                options = [i for i in range(1, 11)],
                value = (
                    default_range_dict["min_evaluation_body"], 
                    default_range_dict["max_evaluation_body"]
                ), 
                on_change = mark_changed_filter,
                kwargs = {"name": "body_evaluation"}
            )

            st.subheader("Evaluation of crema")
            crema_evaluation = st.select_slider(
                "Please select the range",
                key = "crema_evaluation_slider",
                options = [i for i in range(1, 11)],
                value = (
                    default_range_dict["min_evaluation_crema"], 
                    default_range_dict["max_evaluation_crema"]
                ), 
                on_change = mark_changed_filter,
                kwargs = {"name": "crema_evaluation"}
            )

    applied_filters = {}
    for filter_name in st.session_state.espresso_data_applied_filters:
        if st.session_state.espresso_data_applied_filters[filter_name]:
            applied_filters[filter_name] = eval(filter_name)


