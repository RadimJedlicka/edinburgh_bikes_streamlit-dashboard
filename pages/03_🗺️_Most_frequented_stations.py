import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Most frequented stations", 
    page_icon=":world_map:", 
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

stations_count = df_bikes['start_station_name'].drop_duplicates().count()

# ######################## ###################################################
# STREAMLIT PAGE STRUCTURE 
# ######################## ###################################################

st.markdown('''<h1 style='text-align: center; color: black;'>
                Most frequented stations</h1>
                ''', unsafe_allow_html=True
)

st.markdown('<h5>TOP stations</h5>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

TOP = col2.slider(
        'Select number of TOP stations you want to plot on a map:', 
        min_value=1, 
        max_value=int(stations_count), 
        value=10, 
        help='Select number of TOP stations you want to pot on a map:', 
)

df_start = (df_bikes[
    ['start_station_name', 'start_station_latitude', 'start_station_longitude']]
    .assign(bikes_left=1, start_latitude=df_bikes.start_station_latitude, 
                         start_longitude=df_bikes.start_station_longitude)
    .groupby('start_station_name')
    .agg({'bikes_left': 'sum', 'start_latitude': 'mean', 
                               'start_longitude': 'mean'})
    .sort_values('bikes_left', ascending=False)
    .reset_index()
    ).head(TOP)
# set index start from 1 so it corresponds with ranking ;-)
df_start.index += 1

col1.write('''
    Below you can see the list of top stations, where bike rents 
    starts the most. In the second column is the total amount 
    of starts from this station over the whole history of rentals.
    ''')

col1.dataframe(df_start[['start_station_name', 'bikes_left']])

fig = px.scatter_mapbox(
    df_start.head(TOP),
    lat='start_latitude', 
    lon='start_longitude', 
    zoom=10, 
    color=df_start.index,
    size='bikes_left',
    hover_name= 'start_station_name',
    color_continuous_scale = 'reds_r',
    mapbox_style='carto-positron'
)

col2.plotly_chart(fig, use_container_width=True, sharing="streamlit")

# SECOND MAP #################################################################

col1, col2 = st.columns([1, 3])

df_end = (df_bikes[
    ['end_station_name', 'end_station_latitude', 'end_station_longitude']]
    .assign(bikes_arrived=1, end_latitude=df_bikes.end_station_latitude, 
                            end_longitude=df_bikes.end_station_longitude)
    .groupby('end_station_name')
    .agg({'bikes_arrived': 'sum', 'end_latitude': 'mean', 
                                  'end_longitude': 'mean'})
    .sort_values('bikes_arrived', ascending=False)
    .reset_index()
    ).head(TOP)
    # set index start from 1 so it corresponds with ranking ;-)
df_end.index += 1

col1.write('''
    Below you can see the list of top stations, where bike rents 
    end the most. In the second column is the total amount 
    of ends in this station over the whole history of rentals.
    ''')

col1.dataframe(df_end[['end_station_name', 'bikes_arrived']])

fig = px.scatter_mapbox(
    df_end.head(TOP),
    lat='end_latitude', 
    lon='end_longitude', 
    zoom=10, 
    color=df_end.index,
    size='bikes_arrived',
    hover_name='end_station_name',
    color_continuous_scale = 'blues_r',
    mapbox_style='carto-positron'
    )

col2.plotly_chart(fig, use_container_width=True, sharing="streamlit")
