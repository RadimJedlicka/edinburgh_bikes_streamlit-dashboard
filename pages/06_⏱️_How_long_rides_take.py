import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy import create_engine


st.set_page_config(
    page_title="How long rides take", 
    page_icon=":stopwatch:", 
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
#
# df_bikes = pd.read_csv('edinburgh_bikes.csv')

# creating new columns in type = datetime
df_bikes['started_at_dt'] = pd.to_datetime(df_bikes['started_at'])
df_bikes['ended_at_dt'] = pd.to_datetime(df_bikes['ended_at'])

# creating new column by subtracting two columns
df_bikes['time_difference'] = df_bikes['ended_at_dt']\
                            - df_bikes['started_at_dt']

# sorting values to see shortest and longest rides
df_timedif = df_bikes[
    ['started_at', 
     'ended_at', 
     'duration', 
     'time_difference']
    ].sort_values('time_difference')


# ######################## ###################################################
# STREAMLIT PAGE STRUCTURE 
# ######################## ###################################################

st.markdown('''<h1 style='text-align: center; color: black;'>
                How long rides take</h1>
                ''', unsafe_allow_html=True
                )

st.write('''
    To find a distant values, we can transfrom our started_at and 
    ended_at columns into the datetime format and subtract each other. 
    By that we get time_difference where we see how long every ride took 
    in days, hours, etc.''')

st.warning('''
    Warning: Streamlit has Error: Unrecognized type: "Duration" (18).
    According to helpdesk it should be solved soon. We will we ;-).
    Meanwhile you can check the dataframe in this form, but rather skip it
    and watch the charts below ;-)''')

st.code(df_timedif)

st.header('Scatter plot of rides length')

fig = plt.figure()
ax = fig.add_subplot(2,1,2)

plt.scatter(df_timedif['duration'], df_timedif.index)

st.pyplot(fig)

st.write('''
    We expect that most of our rides happens within fisrt hours. 
    Lets trim our plot: Set up the `hours` value = meaning that only
    rides shorter than selected number hours will be plotted. Message below 
    tells how much values you lost with trimming the dataframe.''')

hours = st.slider(
    "Hours",
    value=4,
    min_value=0,
    max_value=27,
)

# calculate, how many values were cut as outlying values
whole_dataframe = df_timedif.shape[0]
trimed_dataframe = df_bikes[df_timedif['duration'] < hours*3600].shape[0]
trimed = 100 - (trimed_dataframe / whole_dataframe * 100)

st.write(f'Percentage of cut rides from plot: {round(trimed, 3)}%')

st.header('Histogram of duration of rides in dataframe')

st.write('''
    When we use tooltip on our histogram of rides, we can see, 
    that most of the rides take between 500 and 600 seconds, 
    which is 8-10 minutes.''')


fig = px.histogram(
    df_timedif,
    x='duration',
    histnorm='percent',
    labels={'duration': 'Duration of rides in seconds'},
    range_x=[0, hours*3600],
    title='Histogram of duration of rides in dataframe',
    width=1000,
    height=500
    )

st.plotly_chart(fig, use_container_width=True)
