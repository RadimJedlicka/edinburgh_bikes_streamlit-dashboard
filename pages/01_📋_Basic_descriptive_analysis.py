import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Basic descriptive analysis", 
    page_icon=":clipboard:", 
    layout="wide", 
    initial_sidebar_state="auto",
)

# ###################################### #####################################
# DATA PROCESSING, DATAFRAMES, VARIABLES 
# ###################################### ##################################### 
# query = 'SELECT * FROM edinburgh_bikes'
# engine = create_engine("mysql+pymysql://data-student:u9AB6hWGsNkNcRDm@data.engeto.com:3306/data_academy_04_2022")
# # save the table as dataframe
# df_bikes = pd.read_sql(sql=query, con=engine)

df_bikes = pd.read_csv('edinburgh_bikes.csv')
df_bikes = df_bikes.drop(columns=['Unnamed: 0'])

df_lat_lon = (df_bikes[
    ['start_station_name', 
    'start_station_latitude', 
    'start_station_longitude']
    ]
    .drop_duplicates()
    .sort_values('start_station_name')
)

df_lat_lon.index += 1

df_lat_lon = df_lat_lon.rename(columns={
    "start_station_latitude": "lat",
    'start_station_longitude': 'lon'}
)

northest = df_bikes.sort_values('start_station_latitude').tail(1)
northest['Position'] = 'northest'
southest = df_bikes.sort_values('start_station_latitude').head(1)
southest['Position'] = 'southest'
easternmost = df_bikes.sort_values('start_station_longitude').tail(1)
easternmost['Position'] = 'easternmost'
westernmost = df_bikes.sort_values('start_station_longitude').head(1)
westernmost['Position'] = 'westernmost'
df_compass = pd.concat([northest, southest, easternmost, westernmost])

# how many stations we have?
stations_count = df_bikes['start_station_name'].drop_duplicates().count()

# ######################## ###################################################
# STREAMLIT PAGE STRUCTURE 
# ######################## ################################################### 

st.markdown('''<h1 style='text-align: center; color: brown;'>
                Basic descriptive analysis</h1>
                ''', 
                unsafe_allow_html=True
)

st.subheader('Descriptive statistics')
st.write(f'''
    First thing, that a good data analyst must do, 
    is to check his dataframe. On this page, we will
    do just that. First we can show first and last
    `n` rows of the dataframe. We can observe that
    our dataframe consisted of {df_bikes.shape[0]} rows
    and {df_bikes.shape[1]} columns.
    First bike was used on {df_bikes.iloc[0, 1]}
    and last ride happened on {df_bikes.iloc[-1, 1]}.''')
st.write('Another interesting statistics follow below.')

st.markdown('<h5>First 5 rows:</h5>', unsafe_allow_html=True)
st.dataframe(df_bikes.head())

st.markdown('<h5>Last 5 rows:</h5>', unsafe_allow_html=True)
st.dataframe(df_bikes.tail())

st.markdown('<h5>Sample of 5 random rows:</h5>', unsafe_allow_html=True)
st.dataframe(df_bikes.sample(n=5,random_state=1))


col1, col2, col3 = st.columns([1,1,2])

col1.markdown('<h5>Column names:</h5>', unsafe_allow_html=True)
col1.dataframe(df_bikes.columns)

col2.markdown('<h5>Missing values:</h5>', unsafe_allow_html=True)
col2.dataframe(df_bikes.isna().sum().sort_values(ascending=False))

col3.markdown('<h5>Descriptive statistics:</h5>', unsafe_allow_html=True)
col3.dataframe(df_bikes.describe().astype(int))


col1, col2, col3 = st.columns([1,1,1])

col1.markdown('<h5>Stations by alphabet:</h5>', unsafe_allow_html=True)


col1.write(f'''
    Because the list of stations would be too long (we have
    {stations_count} stations in the dataset),
    you can select amount of first and last stations
    of this list.''')

number = col1.number_input(
    'Select a number:', 
    value=5,
    min_value=int(1), 
    max_value=stations_count,
    help='The number of stations in alphabetical order will follow',
    )

col2.markdown(f'<h5>First {int(number)} stations:</h5>', unsafe_allow_html=True)
col2.dataframe(df_lat_lon['start_station_name'].head(int(number)))

col3.markdown(f'<h5>Last {int(number)} stations:</h5>', unsafe_allow_html=True)
col3.write(df_lat_lon['start_station_name'].tail(int(number)))



col1, col2 = st.columns([1,3])

col1.markdown('<h5>The most distant stations:</h5>', unsafe_allow_html=True)

option = col1.selectbox(
     'Select most distant station:',
     ('Easternmost', 'Westernmost', 'Southest', 'Northest'))

if option == 'Easternmost':
    col1.dataframe(easternmost['start_station_name'])
if option == 'Westernmost':
    col1.dataframe(westernmost['start_station_name'])
if option == 'Southest':
    col1.dataframe(southest['start_station_name'])
if option == 'Northest':
    col1.dataframe(northest['start_station_name'])


fig = px.scatter_mapbox(
    df_compass,
    lat='start_station_latitude', 
    lon='start_station_longitude', 
    zoom=9, 
    color='Position',
    hover_name= 'start_station_name',
    color_discrete_sequence=['blue', 'red', 'green', 'yellow'],
    mapbox_style='carto-positron',
)

col2.plotly_chart(fig, use_container_width=True, sharing="streamlit")
