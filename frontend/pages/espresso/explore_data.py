import streamlit as st
import pandas as pd
import plotly.express as px
from src.helpers import (
    get_espresso_filter_default_range, 
    get_coffee_dict_from_espresso, 
    get_machine_dict_from_espresso, 
    get_grinder_dict_from_espresso, 
    get_users_espresso_data
)

st.title("Explore Espresso Data")

# get the data from db, convert to df, and correct data types
user_id = st.session_state.current_user_id
user_data = get_users_espresso_data(user_id)
full_df = pd.DataFrame(user_data["data"], columns=user_data["columns"])
full_df["experiment_date"] = pd.to_datetime(full_df["experiment_date"]).dt.date
full_df["experiment_time"] = pd.to_datetime(full_df["experiment_time"]).dt.time
full_df["puck_screen_thickness_mm"] = full_df["puck_screen_thickness_mm"].astype(float)
full_df["grind_level_relative"] = full_df["grind_level_relative"].astype(float)
full_df["dose_gr"] = full_df["dose_gr"].astype(float)
full_df["yield_gr"] = full_df["yield_gr"].astype(float)
full_df["extraction_ratio"] = full_df["extraction_ratio"].astype(float)

###########
# Filters #
###########

# toggle to apply filters
apply_filters = st.toggle("Apply filters?")
if not apply_filters:
    st.session_state.espresso_data_filters_applied = False # reverts if untoggled
# the form to select filters, if toggled:
else:
    # get default values from db
    default_range_dict = get_espresso_filter_default_range(user_id)
    default_coffee_dict = get_coffee_dict_from_espresso(user_id)
    default_machine_dict = get_machine_dict_from_espresso(user_id)
    default_grinder_dict = get_grinder_dict_from_espresso(user_id)

    with st.form("filters", border = True):
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
            coffee_beans = [int(i) for i in coffee_beans]

        with st.expander("Equipment selection"):
            left2, right2 = st.columns([0.5, 0.5])
            with left2:
                coffee_machine = st.multiselect(
                    "Coffee machine",
                    options = default_machine_dict, 
                    default = default_machine_dict, 
                    format_func = lambda x: default_machine_dict[x]
                )
                coffee_machine = [int(i) for i in coffee_machine]
                basket_pressurized = st.multiselect(
                    "Pressurized basket",
                    options = ["yes", "no"], 
                    default = ["yes", "no"],
                )
                portafilter_spout = st.multiselect(
                    "Portafilter spout type",
                    options = ["single", "double", "bottomless"], 
                    default = ["single", "double", "bottomless"],
                )        
            with right2:
                grinder = st.multiselect(
                    "Grinder",
                    options = default_grinder_dict, 
                    default = default_grinder_dict, 
                    format_func = lambda x: default_grinder_dict[x][0]
                )
                grinder = [int(i) for i in grinder]
                basket_shot_size = st.multiselect(
                    "Basket shot size",
                    options = ["single", "double"], 
                    default = ["single", "double"],
                )

        with st.expander("Preparation methods"):
            left3, right3 = st.columns([0.5, 0.5])
            with left3:
                wdt_used = st.multiselect(
                    "WDT used",
                    options = ["yes", "no"], 
                    default = ["yes", "no"],
                )
                puck_screen_used = st.multiselect(
                    "Puck screen used",
                    options = ["yes", "no"], 
                    default = ["yes", "no"],
                )       
            with right3:
                tamping_method = st.multiselect(
                    "Tamping method",
                    options = ["manual", "automatic"], 
                    default = ["manual", "automatic"],
                )
                leveler_used = st.multiselect(
                    "Leveler used",
                    options = ["yes", "no"], 
                    default = ["yes", "no"],
                )
        
        with st.expander("Extraction parameters"):

            st.subheader("Grind level relative to the grinder's espresso range")
            grind_level = st.select_slider(
                "Please select the range",
                key = "grind_level_slider",
                options = [round(i * 0.01, 2) for i in range(
                    int(float(default_range_dict["min_grind_level"])*100), 
                    int(float(default_range_dict["max_grind_level"])*100+1)
                )],
                value = (
                    float(default_range_dict["min_grind_level"]), 
                    float(default_range_dict["max_grind_level"])
                ),
                format_func = lambda x: f"{x:.1f}"
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
                )
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
                format_func = lambda x: f"{x} sec"
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
                )
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
        
        filters_applied = st.form_submit_button("Apply filters")
        st.session_state.espresso_data_filters_applied = filters_applied
# End filters ############################################################

# Subset the full df if filters are applied:
if st.session_state.espresso_data_filters_applied:
    df = full_df[
        (full_df["experiment_date"] >= date_from) & 
        (full_df["experiment_date"] <= date_until) & 
        (full_df["coffee_id"].isin(coffee_beans)) & 
        (full_df["coffee_machine_id"].isin(coffee_machine)) & 
        (full_df["grinder_id"].isin(grinder)) & 
        (full_df["basket_pressurized"].isin(basket_pressurized)) & 
        (full_df["portafilter_spout"].isin(portafilter_spout)) & 
        (full_df["basket_shot_size"].isin(basket_shot_size)) & 
        (full_df["wdt_used"].isin(wdt_used)) & 
        (full_df["puck_screen_used"].isin(puck_screen_used)) & 
        (full_df["tamping_method"].isin(tamping_method)) & 
        (full_df["leveler_used"].isin(leveler_used)) & 
        (full_df["grind_level_relative"] >= grind_level[0]) & 
        (full_df["grind_level_relative"] <= grind_level[1]) & 
        (full_df["dose_gr"] >= dose_gr[0]) & 
        (full_df["dose_gr"] <= dose_gr[1]) & 
        (full_df["extraction_time_sec"] >= extr_time[0]) & 
        (full_df["extraction_time_sec"] <= extr_time[1]) & 
        (full_df["yield_gr"] >= yield_gr[0]) & 
        (full_df["yield_gr"] <= yield_gr[1]) & 
        (full_df["extraction_ratio"] >= extr_ratio[0]) & 
        (full_df["extraction_ratio"] <= extr_ratio[1]) & 
        (full_df["evaluation_general"] >= general_evaluation[0]) & 
        (full_df["evaluation_general"] <= general_evaluation[1]) & 
        (full_df["evaluation_flavor"] >= flavor_evaluation[0]) & 
        (full_df["evaluation_flavor"] <= flavor_evaluation[1]) & 
        (full_df["evaluation_body"] >= body_evaluation[0]) & 
        (full_df["evaluation_body"] <= body_evaluation[1]) & 
        (full_df["evaluation_crema"] >= crema_evaluation[0]) & 
        (full_df["evaluation_crema"] <= crema_evaluation[1])
    ]
else:
    df = full_df

st.header("Dashboard")

# Feature data types, to determine plot types
num_vars = {
    "grind_level_relative" : "Relative grind level",
    "dose_gr" : "Dose (gr)",
    "extraction_time_sec" : "Extraction time (sec)",
    "yield_gr" : "Yield (gr)",
    "extraction_ratio" : "Extraction ratio",
    "evaluation_general" : "General evaluation",
    "evaluation_flavor" : "Flavor evaluation",
    "evaluation_body" : "Body evaluation",
    "evaluation_crema" : "Crema evaluation"
}
cat_vars = {
    "machine_description" : "Coffee machine",
    "grinder_description" : "Grinder",
    "coffee_description" : "Coffee beans",
    "basket_pressurized" : "Pressurized basket",
    "portafilter_spout" : "Portafilter spout type",
    "basket_shot_size" : "Basket shot size",
    "wdt_used" : "WDT used",
    "puck_screen_used" : "Puck screen used",
    "tamping_method" : "Tamping method",
    "leveler_used" : "Leveler used"
}
time_vars = {
    "year_month" : "Experiment date"
}
all_vars = {**num_vars, **cat_vars, **time_vars}

num_counter = 0
cat_counter = 0
time_counter = 0

left_d1, right_d1 = st.columns([0.67, 0.33], vertical_alignment = "bottom")

#initialize variables
y_var = None
x_var = None
z_var = None

# Select the first variable
with left_d1:
    y_var = st.selectbox(
        "Please select a variable to explore:",
        options = all_vars, 
        index = 5,  # Default to "evaluation_general"
        format_func = lambda x: all_vars[x]
    )
    all_vars.pop(y_var)
    # Determine the type of the selected variable
    if y_var in num_vars:
        num_counter += 1
    elif y_var in cat_vars:
        cat_counter += 1
    elif y_var in time_vars:
        time_counter += 1

with right_d1:
    add_second_var = st.toggle(
        "Add a second variable?", 
        value = True
    )

if add_second_var:
    left_d2, right_d2 = st.columns([0.67, 0.33], vertical_alignment = "bottom")
    with left_d2:
        x_var = st.selectbox(
            "Please select a second variable to explore:",
            options = all_vars, 
            index = 4, # Default to "extraction_ratio" 
            format_func = lambda x: all_vars[x]
        )
        all_vars.pop(x_var)
        # Determine the type of the selected variable
        if x_var in num_vars:
            num_counter += 1
        elif x_var in cat_vars:
            cat_counter += 1
        elif x_var in time_vars:
            time_counter += 1

    with right_d2:
        add_third_var = st.toggle(
            "Add a third variable?", 
            value = True
        )

    if add_third_var:
        left_d3, right_d3 = st.columns([0.67, 0.33], vertical_alignment = "bottom")
        with left_d3:
            z_var = st.selectbox(
                "Please select a third variable:",
                options = all_vars, 
                index = 9,  # Default to "coffee_description"
                format_func = lambda x: all_vars[x]
            )
            if z_var in num_vars:
                num_counter += 1
            elif z_var in cat_vars:
                cat_counter += 1
            elif z_var in time_vars:
                time_counter += 1

var_types = (num_counter, cat_counter, time_counter)
all_vars = {**num_vars, **cat_vars, **time_vars}

if "year_month" in [y_var, x_var, z_var]:
    df["year_month"] = pd.to_datetime(df["experiment_date"]).dt.to_period("M").astype(str)

@st.cache_data
def get_plot_data(df, y_var, x_var=None, z_var=None):

    if x_var is None and z_var is None:
        return df[[y_var]]
    elif x_var is not None and z_var is None:
        return df[[y_var, x_var]]
    else:
        return df[[y_var, x_var, z_var]]

@st.cache_data
def get_plot_data_of_counts(df, y_var, x_var=None, z_var=None):
    if x_var is None and z_var is None:
        return df.\
            value_counts(y_var).\
            reset_index(name = "Number of espressos").\
            sort_values(by = y_var).\
            rename(columns = {y_var : all_vars[y_var]})
    elif x_var is not None and z_var is None:
        return df.\
            groupby([y_var, x_var]).\
            size().\
            reset_index(name = "Number of espressos").\
            sort_values(by = y_var).\
            rename(columns = {y_var : all_vars[y_var], x_var : all_vars[x_var]})
    else:
        return df.\
            groupby([y_var, x_var, z_var]).\
            size().\
            reset_index(name = "Number of espressos").\
            sort_values(by = y_var).\
            rename(columns = {y_var : all_vars[y_var], x_var : all_vars[x_var], z_var : all_vars[z_var]})

if var_types == (0, 0, 1):
    plot_data = get_plot_data_of_counts(df, y_var)
    
    fig = px.bar(
        plot_data, 
        x = all_vars[y_var], 
        y = "Number of espressos",
        title = f"Number of espressos per month", 
        labels = {all_vars[y_var] : "Year-Month"}
    )
    st.plotly_chart(fig, use_container_width = True)

elif var_types == (0, 1, 0):
    plot_data = get_plot_data_of_counts(df, y_var)
    
    fig = px.bar(
        plot_data, 
        x = all_vars[y_var], 
        y = "Number of espressos",
        title = f"Number of espressos per {all_vars[y_var]}"
    )
    st.plotly_chart(fig, use_container_width = True)

elif var_types == (0, 1, 1):
    plot_type = "stacked_bar_time"
elif var_types == (0, 2, 0):
    plot_type = "stacked_bar"
elif var_types == (0, 2, 1):
    plot_type = "stacked_bar_time_facet"
elif var_types == (0, 3, 0):
    plot_type = "stacked_bar_facet"
elif var_types == (1, 0, 0):
    plot_type = "histogram"
elif var_types == (1, 0, 1):
    plot_type = "line"
elif var_types == (1, 1, 0):
    plot_type = "violin"
elif var_types == (1, 1, 1):
    plot_type = "line_color"
elif var_types == (1, 2, 0):
    plot_type = "violin_facet"
elif var_types == (2, 0, 0):
    plot_type = "scatter"
elif var_types == (2, 0, 1):
    plot_type = "scatter_color_continous"
elif var_types == (2, 1, 0):
    plot_type = "scatter_color_discrete"
elif var_types == (3, 0, 0):
    plot_type = "scatter_size"

#st.write(f"Plot type: **{plot_type}**")

    


