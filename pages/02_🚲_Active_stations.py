import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Active and inactive stations", 
    page_icon=":bike:", 
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

# ######################## ###################################################
# STREAMLIT PAGE STRUCTURE 
# ######################## ###################################################

st.markdown('''<h1 style='text-align: center; color: black;'>
                Active and inactive stations</h1>
                ''', 
                unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1,3,1])

col2.write('''
    Our analytical team together with the provider - 
    Just Eat Cycles - decided to search for active and especially 
    inactive stations to better understand the needs of the customers. 
    For this purpose, we need to distinguish between often used stations 
    and those with not much of use. We decided to set a time-limit, meaning: 
    how many months ago the station was used for the last time? On the slider 
    you can setup the number of months (default is 12 -> one year).''')

months_ago = col2.slider(
    'Select number of months:', 
    min_value=0, 
    max_value=36, 
    value=12, 
    help='Select the number of months before which the stations were last used', 
)


# Time limit for stations being active according to value from slider
time_limit = df_bikes.iloc[-1, -1] - pd.Timedelta(months_ago*30.4, unit='D')

col2.write(f'''Stations marked by red on the map were not used since 
            {time_limit.date()} (according to chosen time-limit).''')

# When the stations were used for the last time
df_last_time_used = (df_bikes[
    ['started_at_dt', 'start_station_name', 
    'start_station_latitude', 'start_station_longitude']
    ].groupby('start_station_name')).max()

# Create new column is_active according to condition
df_last_time_used['is station active?'] = np.where(
    df_last_time_used['started_at_dt'] > time_limit, 'active', 'inactive')

df_last_time_used.reset_index(inplace=True)

# Plot map of active and inactive stations
fig = px.scatter_mapbox(
    df_last_time_used,
    lat='start_station_latitude', 
    lon='start_station_longitude', 
    zoom=10, 
    width=1200, 
    height=600,
    # title='Active and inactive stations',
    color='is station active?',
    hover_name= 'start_station_name',
    color_discrete_sequence=['green', 'red'],
    mapbox_style='stamen-terrain',
)

st.plotly_chart(fig, use_container_width=True, sharing="streamlit")

col2.markdown('''*You can display one category of stations by clicking 
            on the cat. names in the legend on the right ;-)*''')

