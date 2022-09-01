import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Effect of weather", 
    page_icon=":partly_sunny_rain:", 
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

query2 = 'SELECT * FROM edinburgh_weather'
engine2 = create_engine("mysql+pymysql://data-student:u9AB6hWGsNkNcRDm@data.engeto.com:3306/data_academy_04_2022")
# save the table as dataframe
df_weather = pd.read_sql(sql=query2, con=engine2)

# df_weather = pd.read_csv('edinburgh_weather.csv')


# create new column in datetime format for joining with df_weather
df_bikes['started_at_dt'] = pd.to_datetime(df_bikes['started_at'])
df_bikes['started_at_dt_rounded'] = df_bikes['started_at_dt'].dt.round('H')

# create new column with date and time in timedate format
df_weather['started_at'] = df_weather[['date', 'time']].agg(' '.join, axis=1)
df_weather['started_at_dt'] = pd.to_datetime(df_weather['started_at'])

# joining two dataframes
df_weather = (
    df_bikes.set_index('started_at_dt_rounded')
    .join(df_weather.set_index('started_at_dt'), how='left', lsuffix='_1')
    )

# fill NaN values with ffill method
df_weather = df_weather.fillna(method='ffill')

# reseting index column
df_weather.reset_index()

# calculating moving averages
df_weather['temp[°C]_mov'] = (df_weather['temp[°C]']
                              .rolling(window=10000, center=True)
                              .mean()
                              .round(2)
                              )
df_weather['feels[°C]_mov'] = (df_weather['feels[°C]']
                               .rolling(window=10000, center=True)
                               .mean()
                               .round(2)
                               )
df_weather['humidity[%]_mov'] = (df_weather['humidity[%]']
                                 .rolling(window=10000, center=True)
                                 .mean()
                                 .round(2)
                                 )

# grouping rows by date
df_weather_g = (df_weather[['date', 'temp[°C]', 'temp[°C]_mov', 'feels[°C]',
                            'feels[°C]_mov', 'rain[mm]', 'humidity[%]', 
                            'humidity[%]_mov',]]
                           .groupby('date')
                           .mean()
                           .reset_index()
                           .round(2)
                           )

# Create figure and plot space
fig, axes = plt.subplots(3, 1, figsize=(20, 15))
plt.subplots_adjust(hspace = .01)

# Add x-axis and y-axis
df_weather_g.plot.bar('date', 'rain[mm]', ax=axes[0], 
                      ylabel='precipitation [mm]', 
                      label='precipitation [mm]')

df_weather_g.plot('date', 'temp[°C]', ax=axes[1], 
                  color='pink', 
                  label='temperature [°C]',  
                  ylabel='temperature [°C]')
df_weather_g.plot('date', 'temp[°C]_mov', ax=axes[1], 
                  color='red', 
                  label='temperature [°C] smoothed')
df_weather_g.plot('date', 'feels[°C]_mov', ax=axes[1], 
                  color='brown', 
                  label='feels like [°C]', 
                  xlabel='')

df_weather_g.plot('date', 'humidity[%]', ax=axes[2], 
                  color='lightblue', 
                  label='humidity [%]', 
                  ylabel='humidity [%]')
df_weather_g.plot('date', 'humidity[%]_mov', ax=axes[2], 
                  color='black', 
                  label='humidity [%] smoothed')

# df_time_selection.plot('date', 'mov_avg', ax=axes[3], 
#                        color='purple',
#                        label='moving average of rides', 
#                        xlim=('2018-09-15','2020-10-31'), 
#                        linewidth=3, 
#                        ylabel='rides [count]')

ax=axes[0].set_xticklabels([])
ax=axes[0].get_xaxis().set_visible(False)

ax=axes[1].set_xticklabels([])
ax=axes[1].get_xaxis().set_visible(False)

ax=axes[2].set_xticklabels([])
ax=axes[2].get_xaxis().set_visible(False)

# ######################## ###################################################
# STREAMLIT PAGE STRUCTURE 
# ######################## ###################################################

st.markdown('''<h1 style='text-align: center;'>
                Effect of weather</h1>
                ''', unsafe_allow_html=True
                )

st.write('''
    If we run the following code sequence, we get diagrams showing various 
    weather parameters in Edinburgh over monitored period of time.

    First up is the precipitation bar graph. It can be observed that it 
    rains more in the summer months, but this does not have a significant 
    effect on the trend of renting bikes.

    The second graph is a line graph showing the evolution of temperature. 
    In general, it can be said that temperatures (also feels-like) is higher 
    in the summer months. However, there are positive fluctuations during 
    the year, which can be correlated with positive fluctuations 
    in bike rentals. This is primarily a fluctuation in May 2019, 
    February 2020 and May to June 2020.

    The third line graph shows the development of air humidity. 
    We can observe a beautiful correlation with temperature: 
    In warmer months, humidity decreases, on the contrary, 
    it increases in colder months. Here too, positive anomalies 
    can be observed, which are related to the increased amount 
    of precipitation (June 2019, March 2020).

    As factors of fluctuations not related to the weather, 
    we can probably name the incoming Covid-19 pandemic in 
    March 2020 and the abnormally high increase 
    in the summer months of 2020.
''')

st.pyplot(fig)