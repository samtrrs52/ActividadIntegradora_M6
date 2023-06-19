import streamlit as st
import pandas as pd
import numpy as np
import plotly as px
import calendar
import plotly.figure_factory as ff
from bokeh.plotting import figure
import matplotlib.pyplot as plt

st.title(':red[Police Incident Reports from 2018 to 2020 in San Francisco]')
st.markdown('The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.')
st.markdown('It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district.')    

df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")
data = pd.DataFrame()

data['Year'] = df['Incident Year']
data['Month'] = pd.to_datetime(df['Incident Date']).dt.strftime('%b')
data['Hour'] = pd.to_datetime(df['Incident Time']).dt.strftime('%H')
data['Day'] = df['Incident Day of Week']
data['Police District'] = df['Police District']
data['Neighborhood'] = df['Analysis Neighborhood']
data['Incident Category'] = df['Incident Category']
data['Incident Subcategory'] = df['Incident Subcategory']
data['Resolution'] = df['Resolution']
data['lat'] = df['Latitude']
data['lon'] = df['Longitude']

data = data.dropna()
month_order = list(calendar.month_abbr[1:])
data['Month'] = pd.Categorical(data['Month'], categories=month_order, ordered=True)
weekdays_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
data['Day'] = pd.Categorical(data['Day'], categories=weekdays_order, ordered=True)
data = data.sort_values(['Month', 'Day', 'Hour'])

subset_data2 = data
year_input = st.sidebar.multiselect(
'Year',
data.groupby('Year').count().reset_index()['Year'].tolist())
if len(year_input) > 0:
    subset_data2 = data[data['Year'].isin(year_input)]

subset_data1 = subset_data2
incident_input = st.sidebar.multiselect(
'Incident Category',
data.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
if len(incident_input) > 0:
    subset_data1 = data[data['Incident Category'].isin(incident_input)]

subset_data = subset_data1
resolution_input = st.sidebar.multiselect(
'Resolution',
subset_data1.groupby('Resolution').count().reset_index()['Resolution'].tolist())
if len(resolution_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(resolution_input)]


st.markdown('**Crime locations in San Francisco**')
st.map(subset_data)

tab1, tab2, tab3 = st.tabs(["By area", "By time, date and hour", "By subtype"])

with tab1:
    st.markdown('**Crimes ocurred per Police District**')
    st.bar_chart(subset_data['Police District'].value_counts())
    st.markdown('**Crimes ocurred per Neighborhood**')
    st.bar_chart(subset_data['Neighborhood'].value_counts())
    
with tab2:
    st.markdown('**Crimes ocurred per date**')
    st.line_chart(subset_data['Month'].value_counts())
    st.markdown('**Crimes ocurred per hour (total by selected period)**')
    st.line_chart(subset_data['Hour'].value_counts())
    st.markdown('**Crimes ocurred per day (total by selected period)**')
    st.line_chart(subset_data['Day'].value_counts())

with tab3:
    st.markdown('**Type of crimes committed**')
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())