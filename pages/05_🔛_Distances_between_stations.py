import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import DistanceMetric
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Distances between stations", 
    page_icon=":twisted_rightwards_arrows:", 
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

#Get the list of all stations and their coordinates
df_stations = df_bikes[
    ['start_station_name', 
    'start_station_latitude', 
    'start_station_longitude']
    ].drop_duplicates()

# Convert the Lat/Long degress in Radians
df_stations['start_station_latitude'] = np.radians(df_stations['start_station_latitude'])
df_stations['start_station_longitude'] = np.radians(df_stations['start_station_longitude'])

# Scipy get_metrics()
dist = DistanceMetric.get_metric('haversine')

# Scipy Pairwise()
df_stations[['start_station_latitude','start_station_longitude']].to_numpy()

distances = pd.DataFrame(
    dist.pairwise(
        df_stations[
            ['start_station_latitude',
            'start_station_longitude']
            ].to_numpy())*6373000,  
            columns=df_stations.start_station_name, 
            index=df_stations.start_station_name).astype(int)

distances = distances.loc[:,~distances.columns.duplicated()]


# DataFrame with start and end stations latitudes and longitudes
df_start_end_stations = df_bikes[
    ['start_station_name', 
     'start_station_latitude', 
     'start_station_longitude',
    'end_station_name', 
     'end_station_latitude', 
     'end_station_longitude']
    ].drop_duplicates()


# Let’s create a haversine function using numpy
def haversine_vectorize(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    newlon = lon2 - lon1
    newlat = lat2 - lat1

    haver_formula = np.sin(newlat/2.0)**2 + np.cos(lat1)\
                    * np.cos(lat2) * np.sin(newlon/2.0)**2

    dist = 2 * np.arcsin(np.sqrt(haver_formula ))
    km = 6367000 * dist #6367 for distance in KM (6367000 in metres) 
                        #for miles use 3958
    return km


# Let’s calculate the haversine distance between origin and destination 
# city using numpy vectorize haversine function
haversine_vectorize(df_start_end_stations['start_station_longitude'],
                    df_start_end_stations['start_station_latitude'],
                    df_start_end_stations['end_station_longitude'], 
                    df_start_end_stations['end_station_latitude']
                   )


# Let’s create a new column called 'start-end-distance-metres' 
# and add to the original dataframe
df_start_end_stations['distance'] = haversine_vectorize(
        df_start_end_stations['start_station_longitude'],
        df_start_end_stations['start_station_latitude'],
        df_start_end_stations['end_station_longitude'], 
        df_start_end_stations['end_station_latitude']
        ).astype(int)

# ######################## ###################################################
# STREAMLIT PAGE STRUCTURE 
# ######################## ###################################################

st.markdown('''<h1 style='text-align: center; color: black;'>
                Distances between stations</h1>
                ''', unsafe_allow_html=True
            )

st.write('''Check the distance matrix below which showcase the distance 
    of each of these stations from each other in meters. 
    Pretty cool, ha? :-)''')

st.dataframe(distances)

st.write('''
    Calculated distances between start and end stations for each ride
    in metres. These distances are the theoretical shortest distances
    between the stations, not length of the actual ride.
    For that we would need to have a gps data of each ride.''')

# Show new DataFrame
st.dataframe(df_start_end_stations[[
    'start_station_name',
    'end_station_name', 
    'distance'
     ]])
     
