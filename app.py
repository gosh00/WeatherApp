import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# --- API Configuration ---
API_KEY = "86da0e105224b40c00ea70c6ccd41427"
URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
URL_POLLUTION = "https://api.openweathermap.org/data/2.5/air_pollution"

# --- Streamlit UI ---
st.set_page_config(page_title="Weather & Air Quality App", layout="centered")
st.title("🌤️ Weather & 🌫️ Air Quality Checker")

# City input
city = st.text_input("Enter city name:", "Plovdiv")

# Fetch data only when a city is entered
if city:
    # --- Get Weather Data ---
    weather_params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response_weather = requests.get(URL_WEATHER, params=weather_params)

    if response_weather.status_code == 200:
        weather_data = response_weather.json()
        temp = weather_data['main']['temp']
        desc = weather_data['weather'][0]['description'].title()
        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']

        st.subheader(f"Weather in {city}")
        st.metric("Temperature", f"{temp} °C")
        st.write(f"**Condition:** {desc}")
    else:
        st.error("❌ Failed to fetch weather data. Check the city name.")
        st.stop()

    # --- Get Air Pollution Data ---
    pollution_params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY
    }

    response_pollution = requests.get(URL_POLLUTION, params=pollution_params)

    if response_pollution.status_code == 200:
        pollution_data = response_pollution.json()
        aqi = pollution_data['list'][0]['main']['aqi']
        components = pollution_data['list'][0]['components']

        aqi_level = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }

        st.subheader("Air Quality Index")
        st.metric("AQI", f"{aqi} - {aqi_level.get(aqi)}")

        # Show pollutant concentrations
        df_pollutants = pd.DataFrame(components.items(), columns=["Pollutant", "μg/m³"])
        st.bar_chart(df_pollutants.set_index("Pollutant"))

    else:
        st.error("❌ Failed to fetch air pollution data.")
