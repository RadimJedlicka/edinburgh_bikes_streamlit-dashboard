import streamlit as st
import pandas as pd
import pymysql
from sqlalchemy import create_engine


# download edinburgh_bikes from server 
query = 'SELECT * FROM edinburgh_bikes'
engine = create_engine("mysql+pymysql://data-student:u9AB6hWGsNkNcRDm@data.engeto.com:3306/data_academy_04_2022")
# save the table as dataframe
df_bikes = pd.read_sql(sql=query, con=engine)

# df_bikes = pd.read_csv('edinburgh_bikes.csv')


st.set_page_config(
    page_title="Radim's APP about Edinburgh bikes", 
    page_icon=":wolf:", 
    layout="wide", 
    initial_sidebar_state="auto",
    )

st.markdown('''<h1 style='text-align: center;'>
                Welcome to Edinburgh bikes APP<br>
                created by  Radim Jedlička</h1>
                ''', 
                unsafe_allow_html=True
                )

col1, col2 = st.columns([1,1])

col1.write('''
    In Edinburgh, as in other cities, the "bike sharing" system works - 
    there are stations with bikes in the city, you can borrow one and 
    then return it at another station. The problem is that in some 
    stations bikes regularly accumulate and in others they are missing. 
    The bike operator, Just Eat Cycles, has commissioned a project 
    to make the system more efficient. As a data analyst,your task is 
    to process the relevant data and find out useful information
    ''')
            
col1.markdown('''
    <ul>
        <li> Identify active and inactive stations</li>
        <li> Identify the most frequented stations</li>
        <li> Identify stations where bikes are piling up 
            and stations where they are potentially missing</li>
        <li> Calculate the distances between individual stations</li>
        <li> How long does one loan last?</li>
        <li> Show the evolution of the demand for bike rental over time</li>
        <li> Find out the effect of weather on bike demand</li>
        <li> Do people rent bikes more at the weekend 
            than during working week?</li>
    </ul>''', 
    unsafe_allow_html=True)

col2.image('intro-picture.jpg', 
    caption='Bike-sharing is cool', 
    output_format="auto"
    )

st.write('''The data which we are working with in this app were 
    downloaded from private database. The general code with use of 
    pymysql library is as folows:''')

st.code('''
query = 'SELECT * FROM [table_name]'
engine = create_engine("mysql+pymysql://[username]:[password]@[server_host]:[port]/[database]")
df_bikes = pd.read_sql(sql=query, con=engine)
''')

st.write('You can download sample of the dataframe by clicking the button below.')

query = 'SELECT * FROM edinburgh_bikes LIMIT 1000'
engine = create_engine("mysql+pymysql://data-student:u9AB6hWGsNkNcRDm@data.engeto.com:3306/data_academy_04_2022")
# save the table as dataframe
df_bikes_limited = pd.read_sql(sql=query, con=engine)
df_bikes_limited.to_csv('edinburgh_bikes_limited.csv')


@st.cache
def convert_df(df_bikes):
    return df_bikes_limited.to_csv().encode('utf-8')

csv = convert_df(df_bikes_limited)

st.download_button(
    "DOWNLOAD",
    csv,
    "edinburgh_bikes_limited.csv",
    "text/csv",
    key='browser-data'
)

# st.markdown('''<h2 style='text-align: center; color: blue;'>
#             So what are you waiting for? Lets analyze<br>
#             </h2>
#             ''', unsafe_allow_html=True
#             )

# st.markdown('''<h3 style='text-align: center; color: blue;'>
#             Choose something from the left sidebar :-)</h3>
#             ''', unsafe_allow_html=True
#             )