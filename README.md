# CambridgeshireTraffic
A streamlit dashboard illustrating the change in traffic volume measured by sensors published by Cambridgeshire council

The app is hosted on streamlit cloud. It takes 2 inputs from the user - 
1. traffic type (vehicle or cycle)
2. Sensor location

Based on this the app provides 
1. A map of the selected sensor plus neighbours within a 5km radius
2. A line chart showing granular details per day of the sensor
3. A max and mean graph showing a monthly trend 

Map drawn using Folium
<img width="1156" alt="Screenshot 2021-12-19 at 09 15 23" src="https://user-images.githubusercontent.com/12529897/146669797-ef0807bb-1b39-44e0-a898-06b72a1aa120.png">

Line chart made using plotly express
<img width="1234" alt="Screenshot 2021-12-19 at 09 19 17" src="https://user-images.githubusercontent.com/12529897/146669822-9e7f3100-976b-4806-a600-c03d595e090a.png">

Max and mean charts made using plotly express
<img width="1244" alt="Screenshot 2021-12-19 at 09 20 26" src="https://user-images.githubusercontent.com/12529897/146669856-a6b794f9-e8f6-4b23-88c6-cb5bc2804228.png">

<img width="1240" alt="Screenshot 2021-12-19 at 09 20 42" src="https://user-images.githubusercontent.com/12529897/146669863-8ff1b2d0-df6d-448f-93ad-1153473bbad4.png">
