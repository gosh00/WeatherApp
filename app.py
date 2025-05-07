import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_KEY = "86da0e105224b40c00ea70c6ccd41427"
city = "Plovdiv"

# --- Weather ---
URL_Weather = "https://api.openweathermap.org/data/2.5/weather"
weather_url = f"{URL_Weather}?q={city}&appid={API_KEY}&units=metric"
response_weather = requests.get(weather_url)

if response_weather.status_code == 200:
    weather_data = response_weather.json()
    temperature = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    
    st.subheader(f"Weather in {city}")
    st.write(f"Temperature: {temperature} °C")
    st.write(f"Conditions: {description}")
else:
    st.error("Failed to get weather data")

# --- Air Pollution ---
URL_AirPollution = "https://api.openweathermap.org/data/2.5/air_pollution"
latitude = 42.1354
longitude = 24.7453
pollution_url = f"{URL_AirPollution}?lat={latitude}&lon={longitude}&appid={API_KEY}"
response_pollution = requests.get(pollution_url)

if response_pollution.status_code == 200:
    pollution_data = response_pollution.json()
    aqi = pollution_data['list'][0]['main']['aqi']
    components = pollution_data['list'][0]['components']
    
    aqi_meaning = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }
    
    st.subheader(f"Air Quality in {city}")
    st.write(f"AQI: {aqi} ({aqi_meaning.get(aqi)})")
    
    df = pd.DataFrame(components.items(), columns=["Pollutant", "Concentration (μg/m³)"])
    st.bar_chart(df.set_index("Pollutant"))
else:
    st.error("Failed to get air pollution data")
