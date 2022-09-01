import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Demand for rents", 
    page_icon=":chart:", 
    layout="wide", 
    initial_sidebar_state="auto",
)

# ###################################### #####################################
# DATA PROCESSING, DATAFRAMES, VARIABLES 
# ###################################### ##################################### 
query = 'SELECT * FROM edinburgh_bikes'
engine = create_engine("mysql+pymysql://data-student:u9AB6hWGsNkNcRDm@data.engeto.com:3306/data_academy_04_2022")
# save the table as dataframe
df_bikes = pd.read_sql(sql=query, con=engine)

# df_bikes = pd.read_csv('edinburgh_bikes.csv')

# Adding `Datetime` type columns for better manipulation with dates
df_bikes['started_at_dt'] = pd.to_datetime(df_bikes['started_at'])
df_bikes['ended_at_dt'] = pd.to_datetime(df_bikes['ended_at'])


df_bikes['date'] = df_bikes['started_at_dt'].dt.date
df_bikes['date'] = pd.to_datetime(df_bikes['date'])

# group dataframe by days 
df_rents = df_bikes[['date', 'index']].groupby('date').count().reset_index()

# rename index column to Number of rents
df_rents.rename(columns={"index": "number_of_rents"}, inplace=True)

# ######################## ###################################################
# STREAMLIT PAGE STRUCTURE 
# ######################## ###################################################

st.markdown('''<h1 style='text-align: center; color: black;'>
                Development of demand for bike rentals over time</h1>
                ''', unsafe_allow_html=True
                )

st.write('''
    In this section we will have a graph drawn showing the development of the 
    demand for bicycle rental in Edinburgh. The user is able to choose the 
    time limits of the graph (the oldest date 2018-09-15, the latest date 
    2021-06-30) and also set the smoothness of the curve describing the 
    moving average (the default value is 30. The farther the value is from 
    zero, the smoother the curve will be).
    ''')

from_date = st.date_input(
    'Choose a starting date:', 
    value=(datetime.date(2018, 9, 15)),
    min_value=(datetime.date(2018, 9, 15)),
    max_value=(datetime.date(2021, 6, 29)),
)

to_date = st.date_input(
    'Choose a starting date:', 
    value=(datetime.date(2021, 6, 30)),
    min_value=(datetime.date(2018, 9, 16)),
    max_value=(datetime.date(2021, 6, 30)),
)

slider = st.slider(
    'Smoothness', 
    min_value=1, 
    max_value=60,
    value=30
)

# adding new column with moving average
df_rents['mov_avg'] = df_rents['number_of_rents'].rolling(
                                                    window=slider, 
                                                    center=True
                                                    ).mean().round(2)

df_time_selection = df_rents[
    (df_rents['date'] > str(from_date)) & (df_rents['date'] < str(to_date))]

x = df_time_selection[['date']]
y = df_time_selection[['number_of_rents']]

# Create figure and plot space
fig, ax = plt.subplots(figsize=(20, 10))

# Add x-axis and y-axis
ax.plot(df_time_selection['date'],
        df_time_selection['number_of_rents'],
        color='lightgreen',
        label='number of rents')
ax.plot(df_time_selection['date'],
        df_time_selection['mov_avg'],
        color='red',
        label='moving average')

# Set title and labels for axes
ax.set(xlabel="Date",
    ylabel="Number of rides",
    title="Development of demand for bike rentals over time\nEdinburgh")
ax.legend()

st.pyplot(fig)

