'''
A simple dashboard built using Streamlit and Folium to illustrate the change in the 
traffic volumes before and during the pandemic
'''

import pandas as pd
import streamlit as st 
import plotly
import plotly.express as px
from numpy import cos, sin, arcsin, sqrt
from math import radians
import json
import folium
from streamlit_folium import folium_static


def haversine(row):
	'''
	Calculate distance between selected sensor and all other sensors and filter 
	out those within a 5km radius
	'''
	lon1 = row['lon1']
	lat1 = row['lat1']
	lon2 = row['lon2']
	lat2 = row['lat2']
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * arcsin(sqrt(a)) 
	km = 6367 * c
	return km


if __name__=="__main__":

	df = pd.read_csv('TrafficMonitoringData.csv')
	df = pd.melt(df, id_vars = ['Year', 'Month', 'Date','Road', 'Type',
	            'Lat', 'Lon', 'Total\nVolume'], 
	            value_vars=['12am-6am', '6am-7am', '7am-8am', '8am-9am',
	            '9am-10am', '10am-11am', '11am-12pm', '12pm-1pm', '1pm-2pm', '2pm-3pm',
	            '3pm-4pm', '4pm-5pm', '5pm-6pm', '6pm-7pm', '7pm-8pm', '8pm-9pm',
	            '9pm-10pm', '10pm-11pm', '11pm-12am'])
	df['Year'] = df['Year'].astype(int)
	df['value'] = df['value'].astype(int)
	df.rename(columns = {'Total\nVolume':'Total', 'Lat':'lat','Lon':'lon'}, inplace=True)
	df = df[['Road', 'Year','Month','Date', 'Type', 'lat', 'lon', 'variable', 'value']]
	df['Type'] = df['Type'].str.strip()

	st.title('Cambridgeshire traffic data 2019-2021')
	st.markdown('The source for this dashboard was taken from the following url - \
		https://data.cambridgeshireinsight.org.uk/dataset/cambridgeshire-hourly-automatic-traffic-counter-data-january-2019-august-2021')


	trafficType = st.sidebar.radio("Select mode of transport", df['Type'].unique())
	df = df[df['Type'].isin([trafficType])]
	options = st.sidebar.selectbox('Choose sensors', df['Road'].unique())

	# Creating 2 different subsets of dataframes to calculate the distance for the map
	d1 = df[['Road', 'lat', 'lon']].drop_duplicates()
	d1 = d1[d1['Road'].isin([options])]
	d1.rename(columns={'Road':'from','lat':'lat1','lon':'lon1'}, inplace=True)
	d1.reset_index(inplace=True, drop=True)

	d2 = df[['Road', 'lat', 'lon']].drop_duplicates()
	d2.rename(columns={'Road':'to','lat':'lat2','lon':'lon2'}, inplace=True)
	d2.reset_index(inplace=True, drop=True)

	dist = d1.join(d2, how="outer")
	dist = dist.ffill()

	dist['distance'] = dist.apply(lambda row: haversine(row), axis=1)
	dist = dist[dist['distance']<=5.0]
	
	df = df[df['Road'].isin(dist['to'])]
	df[['c', 'd']] = df['variable'].str.split('-', expand=True)	

	df['start'] = pd.to_datetime(df['c'], format='%I%p').dt.hour

	# Although timeseries index havent been applied, converting to datetime yielded errros in the dates which are now corrected
	df['from'] = df['Date'].astype(str)+'-'+df['Month']+'-'+df['Year'].astype(str)+' '+df['c'].astype(str)
	df['from'] = df['from'].str.replace('Tue 31-April-2020', 'Thu 30-April-2020')
	df['from'] = df['from'].str.replace('Tue 31-June-2020', 'Thu 30-June-2020')
	df['from'] = df['from'].str.replace('Wed 30-February-2021', 'Sun 28-February-2021')
	df['from'] = df['from'].str.replace('Wed 31-September-2019', 'Mon 30-September-2019')
	df['from'] = df['from'].str.replace('Wed 31-November-2019', 'Sat 30-November-2019')
	df['from'] = pd.to_datetime(df['from'])
	df.sort_values(by='from', inplace=True)

	# Drawing the folium map
	mapObj = folium.Map(location=[d1['lat1'], d1['lon1']], zoom_start=12, titles='Traffic sensors within 5km of selection', attr="attribution")
	folium.Circle(location=[d1['lat1'], d1['lon1']], radius=5000).add_to(mapObj)
	dist.apply(lambda row:folium.Marker(location=[row["lat2"], row["lon2"]], tooltip=row['to']).add_to(mapObj), axis=1)
	folium_static(mapObj)

	# Drawing the line chart to allow more granular look
	line = px.line(df, x='from', y='value', markers=True, color='Road', width=800)
	st.plotly_chart(line)

	# Drawing the max and mean charts to illustrate the trends
	df['Month-Year'] = df['Month']+'-'+df['Year'].astype(str)
	monthlyMaxDf = df.groupby(['Road', 'Month-Year'])['value'].max()
	monthlyMaxDf = monthlyMaxDf.reset_index()
	monthlyMaxDf['Month-Year'] = pd.to_datetime(monthlyMaxDf['Month-Year'])
	monthlyMaxDf.sort_values(by='Month-Year', inplace=True)

	monthlyMax = px.line(monthlyMaxDf, x='Month-Year', y='value', color='Road', title = 'Max traffic per month', width=800)
	st.plotly_chart(monthlyMax)

	monthlyAvgDf = df.groupby(['Road', 'Month-Year'])['value'].mean()
	monthlyAvgDf = monthlyAvgDf.reset_index()
	monthlyAvgDf['Month-Year'] = pd.to_datetime(monthlyAvgDf['Month-Year'])
	monthlyAvgDf.sort_values(by='Month-Year', inplace=True)
	monthlyAvg = px.line(monthlyAvgDf, x='Month-Year', y='value', color='Road', title = 'Avg traffic per month', width=800)
	st.plotly_chart(monthlyAvg)

