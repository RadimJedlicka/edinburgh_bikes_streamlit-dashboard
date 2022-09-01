import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Where bikes cummulate", 
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

df_start = (df_bikes[
    ['start_station_name', 'start_station_latitude', 'start_station_longitude']]
    .assign(bikes_left=1, start_latitude=df_bikes.start_station_latitude, 
                        start_longitude=df_bikes.start_station_longitude)
    .groupby('start_station_name')
    .agg({'bikes_left': 'sum', 'start_latitude': 'mean', 
                              'start_longitude': 'mean'})
    .sort_values('bikes_left', ascending=False)
    .reset_index()
    )
df_start.index += 1

df_end = (df_bikes[
    ['end_station_name', 'end_station_latitude', 'end_station_longitude']]
    .assign(bikes_arrived=1, end_latitude=df_bikes.end_station_latitude, 
                        end_longitude=df_bikes.end_station_longitude)
    .groupby('end_station_name')
    .agg({'bikes_arrived': 'sum', 'end_latitude': 'mean', 
                                 'end_longitude': 'mean'})
    .sort_values('bikes_arrived', ascending=False)
    .reset_index()
    )
df_end.index += 1

# join of two tables above to calculate difference between amount of bikes
# that arrived to the stations and those that left the stations.
df_bikes_occupancy = (
    df_start.set_index('start_station_name')
    .join(df_end.set_index('end_station_name'), how='left')
)

# create new column to subtract bikes that left from bikes arrived
df_bikes_occupancy['arrived-left'] = (df_bikes_occupancy['bikes_arrived'] 
                                    - df_bikes_occupancy['bikes_left']
                                    )
df_bikes_occupancy = df_bikes_occupancy.reset_index()
df_bikes_occupancy.sort_values('arrived-left', ascending=False, inplace=True)

##############################################################################

# Adding `Datetime` type columns for better manipulation with dates
df_bikes['started_at_dt'] = pd.to_datetime(df_bikes['started_at'])
df_bikes['ended_at_dt'] = pd.to_datetime(df_bikes['ended_at'])
# add column in date format
df_bikes['date'] = df_bikes['started_at_dt'].dt.date

##############################################################################

# count, how many bikes leave the station, group by day
df_b_left = (df_bikes[['date', 'start_station_name', 
                'start_station_latitude', 'start_station_longitude']]
    .assign(bikes_left_station=1, 
            start_latitude=df_bikes.start_station_latitude, 
            start_longitude=df_bikes.start_station_longitude)
    .groupby(['date', 'start_station_name'])
    .agg({'bikes_left_station': 'sum', 
        'start_latitude': 'mean', 'start_longitude': 'mean'})
    .reset_index()
    )

# add column used for time-slider
df_b_left['date_dt'] = pd.to_datetime(df_b_left['date'])
df_b_left['show_date'] = df_b_left['date_dt'].dt.strftime('%Y-%d-%m')

##############################################################################

# count, how many bikes arrive to station, group by day
df_b_arrived = (df_bikes[['date', 'end_station_name', 
                    'end_station_latitude', 'end_station_longitude']]
    .assign(bikes_arrived_to_station=1, 
            end_latitude=df_bikes.end_station_latitude, 
            end_longitude=df_bikes.end_station_longitude)
    .groupby(['date', 'end_station_name'])
    .agg({'bikes_arrived_to_station': 'sum', 
        'end_latitude': 'mean', 'end_longitude': 'mean'})
    .reset_index()
    )

# add column used for time-slider
df_b_arrived['date_dt'] = pd.to_datetime(df_b_arrived['date'])
df_b_arrived['show_date'] = df_b_arrived['date_dt'].dt.strftime('%Y-%d-%m')

# ######################## ###################################################
# STREAMLIT PAGE STRUCTURE 
# ######################## ###################################################

st.markdown('''<h1 style='text-align: center; color: black;'>
                Where bikes cummulate and lack</h1>
                ''', unsafe_allow_html=True
)

col1, col2 = st.columns([1,3])

col1.subheader('Stations occupancy')

col1.write('''Check out the beautiful map of stations occupancy. 
    <span style='color: red; font-style: italic; font-weight: bold'>
    Warm colors</span> 
    (higher positive values) highligt stations where bikes cummulate. 
    <span style='color: blue; font-style: italic; font-weight: bold'>
    Cold colors</span> 
    (higher negative values) highligt stations where bikes lack. 
    <span style='color: gold; font-style: italic; font-weight: bold'>
    Yellow colors</span>
    (values around zero) mark stations where the equilibrium state 
    of the rents is usually reached.''', 
    unsafe_allow_html=True
    )

# plot map of stations occupancy
fig = px.scatter_mapbox(
    df_bikes_occupancy,
    lat='start_latitude', 
    lon='start_longitude', 
    zoom=10, 
    width=1200, 
    height=600,
    # title='Occupancy of bike stations',
    color='arrived-left',
    hover_name= 'start_station_name',
    color_continuous_scale = 'portland',
    mapbox_style="carto-positron")

col2.plotly_chart(fig, use_container_width=True, sharing="streamlit")

st.subheader('Occupancy of starting locations')
st.write('''
    By using the slider below the map, you can select the day in the history
    of bike rentals in Edinburgh. The circles highlight the stations used
    that day as starting stations. The darkness and size of the circle 
    corresponds to a higher frequency in use on that day.
''')

# Map of bike stations with time-slider - starting locations
fig = px.scatter_mapbox(
    df_b_left,
    lat='start_latitude', 
    lon='start_longitude', 
    zoom=11, 
    width=1200, 
    height=800,
    size='bikes_left_station',
    color='bikes_left_station',
    hover_name= 'start_station_name',
    animation_frame='show_date',
    color_continuous_scale = 'reds',
    mapbox_style='carto-positron',
    )

st.plotly_chart(fig, use_container_width=True, sharing="streamlit")

st.subheader('Occupancy of ending locations')
st.write('''
    By using the slider below the map, you can select the day in the history
    of bike rentals in Edinburgh. The circles highlight the stations used
    that day as ending stations. The darkness and size of the circle 
    corresponds to a higher frequency in use on that day.
''')

# Map of bike stations with time-slider - ending locations
fig = px.scatter_mapbox(
    df_b_arrived,
    lat='end_latitude', 
    lon='end_longitude', 
    zoom=11, 
    width=1200, 
    height=800,
    size='bikes_arrived_to_station',
    color='bikes_arrived_to_station',
    hover_name= 'end_station_name',
    animation_frame='show_date',
    color_continuous_scale = 'blues',
    mapbox_style='carto-positron',
    )

st.plotly_chart(fig, use_container_width=True, sharing="streamlit")
