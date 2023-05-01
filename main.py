import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
import numpy as np

# Load the dataset
@st.cache_data 
def load_data(url):
    df = pd.read_csv(url)
    return df

data = load_data("https://raw.githubusercontent.com/amrhkm/wind-turbine-power-prediction/master/df.csv")

# Load the trained model from the file
@st.cache_resource
def load_model():
  with open('best_rf.pickle', 'rb') as f:
    model = pickle.load(f)
    return model

model = load_model()


# Page header
st.title("Wind Turbine Power Prediction")
st.write(f"Made by Amir Hakim, visit my [data portfolio](https://amrhkm.com/) to view my other projects")

st.header(f"View [original data](https://www.kaggle.com/datasets/berkerisen/wind-turbine-scada-dataset)")
st.write("""
- Date/Time : readings for 10 minutes intervals
- LV ActivePower (kW): The power generated by the turbine for that moment
- Wind Speed (m/s): The wind speed at the hub height of the turbine (the wind speed that turbine use for electricity generation)
- TheoreticalPowerCurve (kW): The theoretical power values that the turbine generates with that wind speed which is given by the turbine manufacturer
- Wind Direction (°): The wind direction at the hub height of the turbine (wind turbines turn to this direction automatically)
""")

data

@st.cache_data
def convert_df(df):
  # IMPORTANT: Cache the conversion to prevent computation on every rerun
  return df.to_csv().encode('utf-8')

csv = convert_df(data)

st.download_button(
    label="Download Processed CSV",
    data=csv,
    file_name='wind_turbine.csv',
    mime='text/csv',
)


st.subheader("Use these slider to make prediction")
# Sliders for input features
wind_speed_ms = st.slider('Wind Speed (m/s)', float(data['wind_speed_ms'].min()), float(data['wind_speed_ms'].max()), step=0.1)
wind_direction_deg = st.slider('Wind Direction (deg)', float(data['wind_direction_deg'].min()), float(data['wind_direction_deg'].max()), step=1.0)
month = st.slider('Month', int(data['month'].min()), int(data['month'].max()))
hour = st.slider('Hour', int(data['hour'].min()), int(data['hour'].max()))
day = st.slider('Day', int(data['day'].min()), int(data['day'].max()))

# Predict button
if st.button('Predict Power'):
    # Create input data from the sliders
    input_data = [[wind_speed_ms, wind_direction_deg, month, day, hour]]
    input_df = pd.DataFrame(input_data, columns=['wind_speed_ms', 'wind_direction_deg', 'month', 'day', 'hour'])

    # Make prediction
    prediction = model.predict(input_df)
    
    # Show prediction
    st.subheader(f"The predicted power output is **:blue[{prediction[0]:.2f}]** kW")
