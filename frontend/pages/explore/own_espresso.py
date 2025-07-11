import streamlit as st

st.title("Explore Own Espresso")

with st.container(border = True):
    st.header("Filters")
    left1, right1 = st.columns([0.5, 0.5], vertical_alignment = "bottom")

    with left1:
        date_from = st.date_input(
            "Date from",
            value = None,
            help = "Select the start date of the data."
        )
    with right1:
        date_until = st.date_input(
            "Date until",
            value = None,
            help = "Select the end date of the data."
        )

    coffee_beans = st.multiselect(
        "Coffee beans",
        options = []
    )

    with st.expander("Equipment selection"):
        left2, right2 = st.columns([0.5, 0.5], vertical_alignment = "top")

        with left2:
            coffee_machine = st.selectbox(
                "Coffee machine",
                options = []
            )
            basket_pressurized = st.radio(
                "Pressurized basket",
                options = ["yes", "no"]
            )
            portafilter_spout = st.radio(
                "Portafilter spout type",
                options = ["single", "double", "bottomless"]
            )
            
        with right2:
            grinder = st.selectbox(
                "Grinder",
                options = []
            )
            basket_shot_size = st.radio(
                "Basket shot size",
                options = ["single", "double"]
            )
    
    with st.expander("Preparation methods"):
        left3, right3 = st.columns([0.5, 0.5], vertical_alignment = "bottom")

        with left3:
            wdt_used = st.radio(
                "WDT used",
                options = ["yes", "no"]
            )
            puck_screen_used = st.radio(
                "Puck screen used",
                options = ["yes", "no"]
            )
            
        with right3:
            tamping_method = st.radio(
                "Tamping method",
                options = ["manual", "automatic"]
            )
            leveler_used = st.radio(
                "Leveler used",
                options = ["yes", "no"]
            )
    
    with st.expander("Extraction parameters"):
        
        st.subheader("Grind level relative to the grinder's espresso range")
        grind_level_from, grind_level_to = st.select_slider(
            "Grind level",
            options = [round(i * 0.1, 1) for i in range(0, 51)],
            value = (0.0, 1.0),
            format_func = lambda x: f"{x:.1f}"
        )
        
        grinder_name = "Baratza Encore ESP"
        range_min = 0.0
        range_max = 20.0
        converted_min = int(grind_level_from * (range_max - range_min) + range_min)
        converted_max = int(grind_level_to * (range_max - range_min) + range_min)
        st.write(f"For grinder **{grinder_name}** the range is from **{converted_min}** to **{converted_max}**")

        st.subheader("Dose (gr)")
        dose_from, dose_to = st.select_slider(
            "Dose",
            options = [round(i * 0.1, 1) for i in range(10, 501)],
            value = (8.0, 24.0),
            format_func = lambda x: f"{x:.1f}"
        )
        left5, right5 = st.columns([0.5, 0.5], vertical_alignment = "bottom")

        st.subheader("Extraction time (seconds)")
        time_from, time_to = st.select_slider(
            "Extraction time",
            options = [i for i in range(1, 121)],
            value = (10, 40),
            format_func = lambda x: f"{x} sec"
        )

        st.subheader("Yield (gr)")
        yield_from, yield_to = st.select_slider(
            "Yield",
            options = [round(i * 0.1, 1) for i in range(10, 1001)],
            value = (10.0, 40.0),
            format_func = lambda x: f"{x:.1f}"
        )

        st.subheader("Extraction ratio")
        ratio_from, ratio_to = st.select_slider(
            "Extraction ratio",
            options = [round(i * 0.01, 2) for i in range(1, 501)],
            value = (1.0, 3.0),
            format_func = lambda x: f"{x:.2f}"
        )



