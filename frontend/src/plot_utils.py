import streamlit as st
import pandas as pd

@st.cache_data
def get_plot_data(
    df : pd.DataFrame, 
    name_mapper : dict, 
    x_var : str, 
    y_var : str | None = None,  
    z_var : str | None = None
    ) -> pd.DataFrame:

    if y_var is None and z_var is None:
        return df[[x_var]].rename(columns = name_mapper)
    elif y_var is not None and z_var is None:
        return df[[x_var, y_var]].rename(columns = name_mapper)
    else:
        return df[[x_var, y_var, z_var]].rename(columns = name_mapper)
    
@st.cache_data
def get_plot_data_with_months(
    df : pd.DataFrame, 
    name_mapper : dict, 
    time_var : str, 
    y_var : str, 
    z_var : str | None = None
    ) -> pd.DataFrame:

    df["month"] = pd.to_datetime(df[time_var]).dt.to_period("M").dt.strftime("%Y-%m")
    df["month_mid"] = (pd.to_datetime(df[time_var]).dt.to_period("M").dt.to_timestamp() + pd.DateOffset(days = 14)).dt.date
    if z_var is None:
        return df[[time_var, y_var, "month", "month_mid"]].rename(columns = name_mapper)
    else:
        return df[[time_var, y_var, z_var, "month", "month_mid"]].rename(columns = name_mapper)


@st.cache_data
def get_plot_data_of_counts(
    df : pd.DataFrame, 
    name_mapper : dict, 
    x_var : str, 
    y_var : str | None = None, 
    z_var : str | None = None
    ) -> pd.DataFrame:

    if y_var is None and z_var is None:
        return df.\
            value_counts(x_var).\
            reset_index(name = "Number of espressos").\
            sort_values(by = x_var).\
            rename(columns = name_mapper)
    elif y_var is not None and z_var is None:
        return df.\
            groupby([x_var, y_var]).\
            size().\
            reset_index(name = "Number of espressos").\
            sort_values(by = x_var).\
            rename(columns = name_mapper)
    else:
        return df.\
            groupby([x_var, y_var, z_var]).\
            size().\
            reset_index(name = "Number of espressos").\
            sort_values(by = x_var).\
            rename(columns = name_mapper)

@st.cache_data
def get_plot_data_of_means(
    df : pd.DataFrame, 
    name_mapper : dict, 
    x_var : str, 
    y_var : str, 
    z_var : str | None = None
    ) -> pd.DataFrame:

    for var in [x_var, y_var, z_var]:
        if var in ["experiment_date"]:
            df[var] = pd.to_datetime(df[var]).dt.to_period("M").astype(str)
    
    if z_var is None:
        return df[[x_var, y_var]].\
            groupby(x_var).\
            mean(y_var).\
            reset_index().\
            rename(columns = name_mapper)
    else:
        return df[[x_var, y_var, z_var]].\
            groupby([x_var, y_var]).\
            mean(z_var).\
            reset_index().\
            rename(columns = name_mapper)