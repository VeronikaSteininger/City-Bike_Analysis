import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime as dt
import folium
from streamlit_folium import st_folium

########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'City Bikes Strategy Dashboard', layout='wide')
st.title("City Bikes Strategy Dashboard")
st.markdown("The dashboard will help to understand the current city-bike situation in New York")
st.markdown("Its aim is to understand user behaviour and to avoid distribution problems")

########################## Import data ###########################################################################################
# CSV einlesen
df = pd.read_csv('citibike_sample_twice_2.5.csv')
# Datum aus der 'day'-Spalte erstellen
df['date'] = pd.to_datetime(df['day'])
print(df[['day', 'date']].head())

top20 = pd.read_csv('top20_stations.csv', index_col = 0)


# ######################################### DEFINE THE CHARTS #####################################################################

## Bar chart
fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)


## Line chart 

df = df.sort_values('date') # bring dates in proper order

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Daily bike rides
fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['bike_rides_daily'],
        name='Daily bike rides',
        line=dict(color='blue')
    ),
    secondary_y=False
)

# Average Temperature
fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['avgTemp'],
        name='Average Temperature',
        line=dict(color='red')
    ),
    secondary_y=True
)

# Achsentitel
fig.update_xaxes(title_text="Year 2022")
fig.update_yaxes(title_text="Bike Rides Daily", secondary_y=False)
fig.update_yaxes(title_text="Average Temperature", secondary_y=True)

# Plot-Titel
fig.update_layout(title_text="Temperature and Trips in 2022", width=900, height=500)


st.plotly_chart(fig, use_container_width=True)

########################## Add maps ###########################

path_to_html = "map_trips_all_year.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in ")
st.components.v1.html(html_data,height=1000)



