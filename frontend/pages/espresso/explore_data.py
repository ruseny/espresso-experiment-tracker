import streamlit as st
import pandas as pd
import plotly.express as px
from src.api_requests import (
    get_espresso_filter_default_range, 
    get_coffee_dict_from_espresso, 
    get_machine_dict_from_espresso, 
    get_grinder_dict_from_espresso, 
    get_users_espresso_data
)
from src.plot_utils import (
    get_plot_data,
    get_plot_data_of_counts, 
    get_plot_data_of_means, 
    get_plot_data_with_months
)

st.title("Explore Espresso Data")

# get the data from db, convert to df, and adjust data types
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

###########################################################################
# Filters #################################################################
###########################################################################

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
# End filters ############################################################

##########################################################################
# Variable selection #####################################################
##########################################################################

st.header("Dashboard")

# Variable data types needed to determine plot types
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
    "experiment_date" : "Experiment date"
}

# a dict to hold all variables names and keys
all_vars = {**num_vars, **cat_vars, **time_vars}
# initialize a dict to hold selected variables
sel_vars = {}

# Initialize counters for variable types
num_counter = 0
cat_counter = 0
time_counter = 0

#initialize variable names
x_var = None
y_var = None
z_var = None

# Select up to three variables, named y, x, and z
# The first variable is always selected, the second and third are optional

left_d1, right_d1 = st.columns([0.67, 0.33], vertical_alignment = "bottom")
# Select the first variable
with left_d1:
    x_var = st.selectbox(
        "Please select a variable to explore:",
        options = all_vars, 
        index = 5,  # Default to "evaluation_general"
        format_func = lambda x: all_vars[x]
    )
    sel_vars[x_var] = all_vars.pop(x_var)
    # Determine the type of the selected variable
    if x_var in num_vars:
        num_counter += 1
    elif x_var in cat_vars:
        cat_counter += 1
    elif x_var in time_vars:
        time_counter += 1

with right_d1:
    add_second_var = st.toggle(
        "Add a second variable?", 
        value = True
    )

if add_second_var:
    left_d2, right_d2 = st.columns([0.67, 0.33], vertical_alignment = "bottom")
    # select the second variable
    with left_d2:
        y_var = st.selectbox(
            "Please select a second variable to explore:",
            options = all_vars, 
            index = 4, # Default to "extraction_ratio" 
            format_func = lambda x: all_vars[x]
        )
        sel_vars[y_var] = all_vars.pop(y_var)
        # Determine the type of the selected variable
        if y_var in num_vars:
            num_counter += 1
        elif y_var in cat_vars:
            cat_counter += 1
        elif y_var in time_vars:
            time_counter += 1

    with right_d2:
        add_third_var = st.toggle(
            "Add a third variable?", 
            value = False
        )

    if add_third_var:
        left_d3, right_d3 = st.columns([0.67, 0.33], vertical_alignment = "bottom")
        # select the third variable
        with left_d3:
            z_var = st.selectbox(
                "Please select a third variable:",
                options = all_vars, 
                index = 9,  # Default to "coffee_description"
                format_func = lambda x: all_vars[x]
            )
            sel_vars[z_var] = all_vars.pop(z_var)
            # Determine the type of the selected variable
            if z_var in num_vars:
                num_counter += 1
            elif z_var in cat_vars:
                cat_counter += 1
            elif z_var in time_vars:
                time_counter += 1

# a tuple to hold variable type counts
var_types = (num_counter, cat_counter, time_counter)

# if date (year-month) is selected, create a variable for months from dates
# if "year_month" in [x_var, y_var, z_var]:
#     df["year_month"] = pd.to_datetime(df["experiment_date"]).dt.to_period("M").astype(str)

# End variable selection #####################################################

#########################################################################
# Plotting ##############################################################
#########################################################################

# Depending on how many of each variable type is selected, determine the plot type

# Plot for only one time variable: bar chart of number of espressos per month
if var_types == (0, 0, 1):
    plot_data = get_plot_data(df, sel_vars, x_var)
    
    fig = px.histogram(
        plot_data, 
        x = sel_vars[x_var], 
        title = f"Number of espressos per month", 
        labels = {sel_vars[x_var] : "Year-Month"}
    )
    fig.update_traces(
        xbins_size = "M1", 
        hovertemplate = "Month and year: %{x|%b %Y} <br>Number of espressos: %{y}"
    )
    fig.update_xaxes(ticklabelmode = "period", dtick = "M1")
    fig.update_yaxes(title_text = "Number of espressos")
    st.plotly_chart(fig, use_container_width = True)

# plot for only one categorical variable: bar chart number of espressos per category
elif var_types == (0, 1, 0):
    plot_data = get_plot_data_of_counts(df, sel_vars, x_var)
    
    fig = px.bar(
        plot_data, 
        x = sel_vars[x_var], 
        y = "Number of espressos",
        title = f"Number of espressos per {sel_vars[x_var]}"
    )
    fig.update_traces(
        hovertemplate = f"{sel_vars[x_var]}: %{{x}} <br>Number of espressos: %{{y}}"
    )
    st.plotly_chart(fig, use_container_width = True)

# plot for one time and one categorical variable: bar chart of number of espressos per month
# color-stacked by categories 
# time is always on x-axis, irrespective of the order of selection
elif var_types == (0, 1, 1):
    cat_var, time_var = None, None
    for var in sel_vars:
        if var in cat_vars:
            cat_var = var
        elif var in time_vars:
            time_var = var

    plot_data = get_plot_data(df, sel_vars, time_var, cat_var)

    fig = px.histogram(
        plot_data,
        x = sel_vars[time_var],
        color = sel_vars[cat_var],
        title = f"Number of espressos per Year-Month and {sel_vars[cat_var]}",
        labels = {sel_vars[time_var] : "Year-Month"}
    )
    fig.update_traces(
        xbins_size = "M1", 
        customdata = plot_data[[sel_vars[cat_var]]], 
        hovertemplate = f"Month and year: %{{x|%b %Y}} <br>{sel_vars[cat_var]}: %{{customdata[0]}} <br>Number of espressos: %{{y}} <extra></extra>"
        )
    fig.update_xaxes(ticklabelmode = "period", dtick = "M1")
    fig.update_yaxes(title_text = "Number of espressos")
    st.plotly_chart(fig, use_container_width = True)

# plot for two categorical variables: bar chart of number of espressos per first categories
# color-stacked by second categories
elif var_types == (0, 2, 0):
    plot_data = get_plot_data_of_counts(df, sel_vars, x_var, y_var)

    fig = px.bar(
        plot_data,
        x = sel_vars[x_var],
        y = "Number of espressos",
        color = sel_vars[y_var],
        title = f"Number of espressos per {sel_vars[x_var]} and {sel_vars[y_var]}",
    )
    fig.update_traces(
        customdata = plot_data[[sel_vars[y_var]]],
        hovertemplate = f"{sel_vars[x_var]}: %{{x}} <br>{sel_vars[y_var]}: %{{customdata[0]}} <br>Number of espressos: %{{y}} <extra></extra>"
    )
    st.plotly_chart(fig, use_container_width = True)

# plot for two categorical variables and one time variable: bar chart of number of espressos per rmonth
# color-stacked by first category, faceted by second category
# time is always on x-axis, irrespective of the order of selection
elif var_types == (0, 2, 1):
    cat_var1, cat_var2, time_var = None, None, None
    for var in sel_vars:
        if var in cat_vars and cat_var1 is None:
            cat_var1 = var
        elif var in cat_vars and cat_var2 is None:
            cat_var2 = var
        elif var in time_vars:
            time_var = var

    plot_data = get_plot_data(df, sel_vars, time_var, cat_var1, cat_var2) 

    # to dynamically change the height of the plot based on the number of facets
    num_facets = len(plot_data[sel_vars[cat_var2]].unique())

    fig = px.histogram(
        plot_data,
        x = sel_vars[time_var],
        color = sel_vars[cat_var1],
        facet_row = sel_vars[cat_var2],
        height = num_facets * 450,
        title = f"Number of espressos per Year-month, {sel_vars[cat_var1]} and {sel_vars[cat_var2]}",
        labels = {sel_vars[time_var] : "Year-Month"}
    )
    fig.update_traces(
        xbins_size = "M1", 
        customdata = plot_data[[sel_vars[cat_var1]]],
        hovertemplate = f"Month and year: %{{x|%b %Y}} <br>{sel_vars[cat_var1]}: %{{customdata[0]}} <br>Number of espressos: %{{y}} <extra></extra>"
    )
    fig.update_xaxes(ticklabelmode = "period", dtick = "M1")
    fig.update_yaxes(title_text = "Number of espressos")
    st.plotly_chart(fig, use_container_width = True)

# plot for three categorical variables: bar chart of number of espressos per first categories,
# color-stacked by second categories, and faceted by third categories
elif var_types == (0, 3, 0):
    plot_data = get_plot_data_of_counts(df, sel_vars, x_var, y_var, z_var)

    num_facets = len(plot_data[sel_vars[z_var]].unique())

    fig = px.bar(
        plot_data, 
        x = sel_vars[x_var], 
        y = "Number of espressos", 
        color = sel_vars[y_var], 
        facet_row = sel_vars[z_var], 
        height = num_facets * 450, 
        title = f"Number of espressos per {sel_vars[x_var]}, {sel_vars[y_var]}, and {sel_vars[z_var]}"
    )
    fig.update_traces(
        customdata = plot_data[[sel_vars[y_var], sel_vars[z_var]]],
        hovertemplate = f"{sel_vars[x_var]}: %{{x}} <br>{sel_vars[y_var]}: %{{customdata[0]}} <br>{sel_vars[z_var]}: %{{customdata[1]}} <br>Number of espressos: %{{y}} <extra></extra>"
    )
    st.plotly_chart(fig, use_container_width = True)

# plot for only one numeric variable: histogram
elif var_types == (1, 0, 0):
    plot_data = get_plot_data(df, sel_vars, x_var)

    fig = px.histogram(
        plot_data, 
        x = sel_vars[x_var], 
        title = "Distribution of " + sel_vars[x_var]
    )
    fig.update_yaxes(title_text = "Number of espressos")
    fig.update_traces(
        hovertemplate = f"{sel_vars[x_var]}: %{{x}} <br>Number of espressos: %{{y}}"
    )
    st.plotly_chart(fig, use_container_width = True)

# plot for one numeric and one time variable: scatter plot with average line
# with points for individual espressos, with time on x-axis, numeric on y-axis
elif var_types == (1, 0, 1):
    num_var, time_var = None, None
    for var in sel_vars:
        if var in num_vars:
            num_var = var
        elif var in time_vars:
            time_var = var

    plot_data_dots = get_plot_data(df, sel_vars, time_var, num_var)
    plot_data_line = get_plot_data_of_means(df, sel_vars, time_var, num_var)
    plot_data_line = get_plot_data_with_months(plot_data_line, sel_vars, sel_vars[time_var], sel_vars[num_var])

    fig_dots = px.scatter(
        plot_data_dots, 
        x = sel_vars[time_var],
        y = sel_vars[num_var],
        title = f"{sel_vars[num_var]} over time"
    )
    fig_dots.update_traces(
        name = "Espressos",
        showlegend = True, 
        hovertemplate = f"{sel_vars[time_var]}: %{{x}} <br>{sel_vars[num_var]}: %{{y:.2f}} <extra></extra>"
        )
    fig_dots.update_xaxes(
        ticklabelmode = "period", 
        dtick = "M1"
    )
    fig_line = px.line(
        plot_data_line, 
        x = "month_mid", 
        y = sel_vars[num_var],
        labels = {"month_mid" : "Year-month"},
        markers = True
    )
    fig_line.update_traces(
        name = "Monthly average",
        showlegend = True,
        marker = dict(
            size = 8, color = "orangered", symbol = "square", 
            line = dict(width = 0.5, color = "dimgray")
        ), 
        line = dict(width = 2, color = "orangered"), 
        hovertemplate = "Month and year: %{x|%b %Y} <br>" + f"Avg. {sel_vars[num_var]}: " + "%{y:.2f}" + "<extra></extra>"
    )
    fig_dots.add_traces(
        fig_line.data
    )
    
    st.plotly_chart(fig_dots, use_container_width = True)

# plot for one numeric and one categorical variable: bee-swarm with average markers
elif var_types == (1, 1, 0):
    cat_var, num_var = None, None
    for var in sel_vars:
        if var in cat_vars:
            cat_var = var
        elif var in num_vars:
            num_var = var

    plot_data_dots = get_plot_data(df, sel_vars, cat_var, num_var)
    plot_data_avg = get_plot_data_of_means(df, sel_vars, cat_var, num_var)

    fig_dots = px.strip(
        plot_data_dots, 
        x = sel_vars[cat_var],
        y = sel_vars[num_var],
        title = f"{sel_vars[num_var]} per {sel_vars[cat_var]}",
    )
    fig_dots.update_traces(
        jitter = 1, 
        name = "Espressos",
        showlegend = True, 
        hovertemplate = f"{sel_vars[cat_var]}: %{{x}} <br>{sel_vars[num_var]}: %{{y:.2f}}<extra></extra>"
    )
    fig_avg = px.scatter(
        plot_data_avg, 
        x = sel_vars[cat_var], 
        y = sel_vars[num_var],
    )
    fig_avg.update_traces(
        marker = dict(
            size = 8, color = "orangered", symbol = "square", 
            line = dict(width = 0.5, color = "dimgray")
        ), 
        name = "Average per category",  
        showlegend = True, 
        hovertemplate = f"{sel_vars[cat_var]}: %{{x}} <br>Avg. {sel_vars[num_var]}: %{{y:.2f}}<extra></extra>"
    )
    fig_dots.add_traces(fig_avg.data)
    st.plotly_chart(fig_dots, use_container_width = True)

# plot for one numeric, one categorical, and one time variable: scatter plot with trend line of average
# with points for individual espressos, with time on x-axis, numeric on y-axis
# and colored by categories
elif var_types == (1, 1, 1):
    cat_var, num_var, time_var = None, None, None
    for var in sel_vars:
        if var in cat_vars:
            cat_var = var
        elif var in num_vars:
            num_var = var
        elif var in time_vars:
            time_var = var
    
    plot_data_dots = get_plot_data(df, sel_vars, time_var, num_var, cat_var)
    plot_data_line = get_plot_data_of_means(df, sel_vars, time_var, num_var)
    plot_data_line = get_plot_data_with_months(plot_data_line, sel_vars, sel_vars[time_var], sel_vars[num_var])

    fig_dots = px.scatter(
        plot_data_dots, 
        x = sel_vars[time_var],
        y = sel_vars[num_var],
        color = sel_vars[cat_var],
        title = f"{sel_vars[num_var]} over time and {sel_vars[cat_var]}",
    )
    fig_dots.update_xaxes(
        ticklabelmode = "period", 
        dtick = "M1"
    )
    fig_dots.update_traces(
        customdata = plot_data_dots[[sel_vars[cat_var]]],
        hovertemplate = f"{sel_vars[time_var]}: %{{x}} <br>{sel_vars[cat_var]}: %{{customdata[0]}} <br>{sel_vars[num_var]}: %{{y:.2f}}<extra></extra>"
    )
    fig_line = px.line(
        plot_data_line, 
        x = "month_mid", 
        y = sel_vars[num_var],
        labels = {"month_mid" : "Year-month"},
        markers = True,
        hover_data = {"month_mid" : "|%b %Y"}
    )
    fig_line.update_traces(
        name = "Monthly average",
        showlegend = True,
        marker = dict(
            size = 8, color = "orangered", symbol = "square", 
            line = dict(width = 0.5, color = "dimgray")
        ), 
        line = dict(width = 2, color = "orangered"), 
        hovertemplate = "Month and year: %{x|%b %Y} <br>" + f"Avg. {sel_vars[num_var]}: " + "%{y:.2f}"
    )
    fig_dots.add_traces(
        fig_line.data
    )
    
    st.plotly_chart(fig_dots, use_container_width = True)

# plot for one numeric and two categorical variables: bee-swarm with average markers
# with points for individual espressos, with numeric on y-axis, first categorical on x-axis,
# and second categorical as color
elif var_types == (1, 2, 0):
    num_var, cat_var1, cat_var2 = None, None, None
    for var in sel_vars:
        if var in num_vars:
            num_var = var
        elif var in cat_vars and cat_var1 is None:
            cat_var1 = var
        elif var in cat_vars and cat_var2 is None:
            cat_var2 = var
    
    plot_data_dots = get_plot_data(df, sel_vars, cat_var1, cat_var2, num_var)
    plot_data_avg = get_plot_data_of_means(df, sel_vars, cat_var1, num_var)

    fig_dots = px.strip(
        plot_data_dots, 
        x = sel_vars[cat_var1],
        y = sel_vars[num_var],
        color = sel_vars[cat_var2],
        title = f"{sel_vars[num_var]} per {sel_vars[cat_var1]} and {sel_vars[cat_var2]}",
    )
    fig_dots.update_traces(
        jitter = 1,
        customdata = plot_data_dots[[sel_vars[cat_var2]]],
        hovertemplate = f"{sel_vars[cat_var1]}: %{{x}} <br>{sel_vars[cat_var2]}: %{{customdata[0]}} <br>{sel_vars[num_var]}: %{{y:.2f}}<extra></extra>"
    )
    fig_avg = px.scatter(
        plot_data_avg, 
        x = sel_vars[cat_var1], 
        y = sel_vars[num_var]
    )
    fig_avg.update_traces(
        marker = dict(
            size = 8, symbol = "square", color = "orangered", 
            line = dict(width = 0.5, color = "dimgray")
        ), 
        name = f"Average per {sel_vars[cat_var1]}",  
        showlegend = True, 
        hovertemplate = f"{sel_vars[cat_var1]}: %{{x}} <br>Avg. {sel_vars[num_var]}: %{{y:.2f}}<extra></extra>"
    )
    fig_dots.add_traces(fig_avg.data)

    st.plotly_chart(fig_dots, use_container_width = True)

# plot for two numeric variables: scatter plot with trend line
elif var_types == (2, 0, 0):
    plot_data = get_plot_data(df, sel_vars, x_var, y_var)

    fig = px.scatter(
        plot_data, 
        x = sel_vars[x_var], 
        y = sel_vars[y_var],
        opacity = 0.2,
        title = f"{sel_vars[y_var]} vs {sel_vars[x_var]}", 
        trendline = "lowess",
    )
    fig.update_traces(
        line = dict(width = 1, color = "orangered"),
        marker = dict(size = 5),
        hovertemplate = f"{sel_vars[x_var]}: %{{x:.2f}} <br>{sel_vars[y_var]}: %{{y:.2f}}"
    )
    st.plotly_chart(fig, use_container_width = True)

# plot for two numeric variables and one time variable: scatter plot with trend line of average
# with points for individual espressos, with time on x-axis, first numeric on y-axis,
# and second numeric as color
elif var_types == (2, 0, 1):
    num_var1, num_var2, time_var = None, None, None
    for var in sel_vars:
        if var in num_vars and num_var1 is None:
            num_var1 = var
        elif var in num_vars and num_var2 is None:
            num_var2 = var
        elif var in time_vars:
            time_var = var
    
    plot_data_dots = get_plot_data(df, sel_vars, time_var, num_var1, num_var2)
    plot_data_line = get_plot_data_of_means(df, sel_vars, time_var, num_var1)
    plot_data_line = get_plot_data_with_months(plot_data_line, sel_vars, sel_vars[time_var], sel_vars[num_var1])

    fig_dots = px.scatter(
        plot_data_dots,
        x = sel_vars[time_var],
        y = sel_vars[num_var1],
        color = sel_vars[num_var2],
        title = f"{sel_vars[num_var1]} over time and {sel_vars[num_var2]}"
    )
    fig_dots.update_xaxes(
        ticklabelmode = "period", 
        dtick = "M1"
    )
    fig_dots.update_traces(
        customdata = plot_data_dots[[sel_vars[num_var2]]],
        hovertemplate = f"{sel_vars[time_var]}: %{{x}} <br>{sel_vars[num_var2]}: %{{customdata[0]}} <br>{sel_vars[num_var1]}: %{{y:.2f}}<extra></extra>"
    )
    fig_line = px.line(
        plot_data_line, 
        x = "month_mid", 
        y = sel_vars[num_var1],
        markers = True
    )
    fig_line.update_traces(
        name = "Monthly average",
        showlegend = True,
        marker = dict(
            size = 8, color = "orangered", symbol = "square", 
            line = dict(width = 0.5, color = "dimgray")
        ), 
        line = dict(width = 2, color = "orangered"), 
        hovertemplate = "Month and year: %{x|%b %Y} <br>" + f"Avg. {sel_vars[num_var1]}: " + "%{y:.2f}" + "<extra></extra>"
    )
    fig_dots.add_traces(fig_line.data)

    st.plotly_chart(fig_dots, use_container_width = True)

# plot for two numeric variables and one categorical variable: scatter plot with trend line
# with points for individual espressos, with first numeric on x-axis, second numeric on y-axis,
# and categorical as color
elif var_types == (2, 1, 0):
    num_var1, num_var2, cat_var = None, None, None
    for var in sel_vars:
        if var in num_vars and num_var1 is None:
            num_var1 = var
        elif var in num_vars and num_var2 is None:
            num_var2 = var
        elif var in cat_vars:
            cat_var = var
    
    plot_data = get_plot_data(df, sel_vars, cat_var, num_var1, num_var2)
    plot_data_avg = get_plot_data_of_means(df, sel_vars, cat_var, num_var1)

    fig = px.scatter(
        plot_data, 
        x = sel_vars[num_var1],
        y = sel_vars[num_var2],
        color = sel_vars[cat_var],
        trendline = "lowess",
        trendline_scope = "overall",
        title = f"{sel_vars[num_var2]} vs {sel_vars[num_var1]} per {sel_vars[cat_var]}",
    )
    fig.update_traces(
        customdata = plot_data[[sel_vars[cat_var]]],
        hovertemplate = f"{sel_vars[num_var1]}: %{{x}} <br>{sel_vars[cat_var]}: %{{customdata[0]}} <br>{sel_vars[num_var2]}: %{{y:.2f}}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width = True)

# plot for three numeric variables: scatter plot with trend line
# with points for individual espressos, with first numeric on x-axis, second numeric on y-axis,
# and third numeric as color
elif var_types == (3, 0, 0):
    plot_data = get_plot_data(df, sel_vars, x_var, y_var, z_var)

    fig = px.scatter(
        plot_data, 
        x = sel_vars[x_var], 
        y = sel_vars[y_var],
        color = sel_vars[z_var],
        trendline = "lowess",
        title = f"{sel_vars[y_var]} vs {sel_vars[x_var]} per {sel_vars[z_var]}",
    )
    fig.update_traces(
        customdata = plot_data[[sel_vars[z_var]]],
        hovertemplate = f"{sel_vars[x_var]}: %{{x}} <br>{sel_vars[z_var]}: %{{customdata[0]}} <br>{sel_vars[y_var]}: %{{y:.2f}}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width = True)

# End plotting ############################################################

    


