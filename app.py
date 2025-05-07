import streamlit as st #web приложение
import requests #връзка с API
import pandas as pd
import matplotlib.pyplot as pet

API_KEY = "86da0e105224b40c00ea70c6ccd41427"
URL_Weather = "https://api.openweathermap.org/data/2.5/weather"
URL_AirPollution = "http://api.openweathermap.org/data/2.5/air_pollution"

city = "Plovdiv"

request_url_weather = f"{URL_Weather}?q={city}&appid={API_KEY}&units=metric"

response_weather = requests.get(request_url_weather)

if response_weather.status_code == 200:
    data = response_weather.json()
    aqi = data['list'][0]['main']['aqi']
    components = data['list'][0]['components']
    
    print(f"AQI (Air Quality Index): {aqi}")
    print("Pollutant Concentrations (μg/m³):")
    for k, v in components.items():
        print(f"  {k}: {v}")
else:
    print(f"Failed to get air pollution data: {response.status_code}")\

latitude = 42.1354
longitude = 24.7453

request_url_pollution = f"{URL_AirPollution}?lat={latitude}&lon={longitude}&appid={API_KEY}"

response_airpollution = requests.get(request_url_pollution)

if response_airpollution.status_code == 200:
    data = response_airpollution.json()
    aqi = data['list'][0]['main']['aqi']
    components = data['list'][0]['components']
    
    # AQI Meaning
    aqi_meaning = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }

    print(f"Air Quality in Plovdiv:")
    print(f"  AQI: {aqi} ({aqi_meaning.get(aqi, 'Unknown')})")
    print("  Pollutants (μg/m³):")
    for pollutant, value in components.items():
        print(f"    {pollutant.upper()}: {value}")
else:
    print(f"Failed to get air pollution data: {response.status_code}")
