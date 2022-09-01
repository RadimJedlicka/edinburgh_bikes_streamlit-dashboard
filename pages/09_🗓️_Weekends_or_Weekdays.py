import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Weekends or Weekdays", 
    page_icon=":calendar:", 
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

df_bikes['started_at_dt'] = pd.to_datetime(df_bikes['started_at'])

# create new column with names of days
df_bikes['day_of_week'] = df_bikes['started_at_dt'].dt.day_name()

# grouping dataset by day names and setting their count
df_weekday = df_bikes[
    ['index', 'day_of_week']
    ].groupby('day_of_week').count().reset_index()
# sorting by index (count)
df_weekday = df_weekday.sort_values('index')

# renaming day names to their shortcuts (better for plotting)
df_weekday=df_weekday.replace(
    {'Monday': 'Mon',
     'Tuesday': 'Tue',
     'Wednesday': 'Wed',
     'Thursday': 'Thu',
     'Friday': 'Fri',
     'Saturday': 'Sat',
     'Sunday': 'Sun',
     }
)

# ######################## ###################################################
# STREAMLIT PAGE STRUCTURE 
# ######################## ###################################################
st.markdown('''<h1 style='text-align: center;'>
                Weekdays or weekends</h1>
                ''', unsafe_allow_html=True
                )
                
st.write('''
    Bellow you can see a histogram 
    that compares the number of rents during the days of the week, 
    sorted by their count from lowest to highest. According to the 
    height of the columns, we can see that the fewest bikes are rented 
    on Monday (first column of the diagram), with the number of rentals 
    increasing as the weekend approaches. Most loans are made on Saturdays. 

    To exactly answer the question asked: Yes, people rent bikes 
    more on weekends (last two columns with highest counts).''')

# Create figure and plot space
fig, ax = plt.subplots(figsize=(10, 5));
# Add x-axis and y-axis
df_weekday.plot.bar(
    'day_of_week', 
    'index', 
    ax=ax, 
    color='red', 
    label='rides per day');

ax.set_ylim(bottom=50000)
ax.set(xlabel="Days in week",
       ylabel="Number of rides",
       title="Comparison of the number of rides for each day of the week\nEdinburgh")

st.pyplot(fig)