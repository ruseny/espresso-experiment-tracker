import streamlit as st

@st.cache_data
def get_plot_data(df, y_var, x_var=None, z_var=None):

    if x_var is None and z_var is None:
        return df[[y_var]]
    elif x_var is not None and z_var is None:
        return df[[y_var, x_var]]
    else:
        return df[[y_var, x_var, z_var]]

@st.cache_data
def get_plot_data_of_counts(df, name_mapper, y_var, x_var = None, z_var = None):
    if x_var is None and z_var is None:
        return df.\
            value_counts(y_var).\
            reset_index(name = "Number of espressos").\
            sort_values(by = y_var).\
            rename(columns = {y_var : name_mapper[y_var]})
    elif x_var is not None and z_var is None:
        return df.\
            groupby([y_var, x_var]).\
            size().\
            reset_index(name = "Number of espressos").\
            sort_values(by = y_var).\
            rename(columns = {y_var : name_mapper[y_var], x_var : name_mapper[x_var]})
    else:
        return df.\
            groupby([y_var, x_var, z_var]).\
            size().\
            reset_index(name = "Number of espressos").\
            sort_values(by = y_var).\
            rename(columns = {y_var : name_mapper[y_var], x_var : name_mapper[x_var], z_var : name_mapper[z_var]})
