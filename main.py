import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle


# Load the dataset
data = pd.read_csv("df.csv")

# Load the trained model from the file
with open('best_rf.pickle', 'rb') as f:
    model = pickle.load(f)

# Split the dataset into features and target variable
#features = ['power_kw', 'wind_speed_ms', 'wind_direction_deg', 'month', 'day', 'hour'] #without theoretical power 

# training_data = data[features]
# X = training_data.drop(columns=['power_kw'], axis = 1).values
# y = training_data['power_kw'].values

# Train a random forest model
# model = RandomForestRegressor()
# model.fit(X, y)

# Sidebar header
st.sidebar.header("Wind Turbine Power Prediction")

# Sidebar sliders for input features
with st.sidebar:
    wind_speed_ms = st.slider('Wind Speed (m/s)', float(data['wind_speed_ms'].min()), float(data['wind_speed_ms'].max()), step=0.1)
    #theoretical_power_kw = st.slider('Theoretical Power (kW)', float(data['theoretical_power_kw'].min()), float(data['theoretical_power_kw'].max()), step=0.1)
    wind_direction_deg = st.slider('Wind Direction (deg)', float(data['wind_direction_deg'].min()), float(data['wind_direction_deg'].max()), step=1.0)
    hour = st.slider('Hour', int(data['hour'].min()), int(data['hour'].max()))
    month = st.slider('Month', int(data['month'].min()), int(data['month'].max()))
    day = st.slider('Day', int(data['day'].min()), int(data['day'].max()))

# Predict button
if st.sidebar.button('Predict Power'):
    # Create input data from the sidebar sliders
    input_data = [[wind_speed_ms, wind_direction_deg, month, day, hour]]
    input_df = pd.DataFrame(input_data, columns=['wind_speed_ms', 'wind_direction_deg', 'month', 'day', 'hour'])
    
    # Make prediction
    prediction = model.predict(input_df)
    
    # Show prediction
    st.write(f"The predicted power output for the wind turbine is {prediction[0]:.2f} kW")
