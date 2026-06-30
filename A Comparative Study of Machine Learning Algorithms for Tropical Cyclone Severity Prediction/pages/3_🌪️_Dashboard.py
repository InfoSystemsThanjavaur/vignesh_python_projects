import streamlit as st

import streamlit as st
import pandas as pd
import joblib
import requests
import numpy as np
import folium
import json
from streamlit_folium import st_folium
import plotly.graph_objects as go
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ===================================================================
# SECURITY CHECK: This is the most important part!
# ===================================================================
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("🔒 Please log in to access this page.")
    st.stop()  # Stop the rest of the script from running

# If the script continues, the user is logged in.
st.success(f"Logged in as **{st.session_state['username']}**")
st.markdown("---")


# -------------------------------------------------------------------


# -------------------------------------------------------------------
# 2. INITIAL SETUP (Functions, Data Loading etc.)
# -------------------------------------------------------------------
@st.cache_resource
def load_all_models():
    models = {}
    model_names = ["Random Forest", "XGBoost", "SVM", "Logistic Regression"]
    for name in model_names:
        try:
            filename = f"{name.lower().replace(' ', '_')}_model.joblib"
            models[name] = joblib.load(filename)
        except FileNotFoundError:
            st.error(f"Model file not found: {filename}")
            models[name] = None
    return models
    
@st.cache_data
def load_performance_data():
    try:
        with open("model_performance.json", "r") as f:
            return pd.DataFrame.from_dict(json.load(f), orient='index')
    except FileNotFoundError:
        return None

try:
    LABEL_ENCODER = joblib.load("label_encoder.joblib")
except FileNotFoundError:
    st.error("`label_encoder.joblib` not found. Predictions will be numeric.")
    LABEL_ENCODER = None
    
@st.cache_data
def load_historical_data():
    """Loads historical cyclone data from a CSV file."""
    try:
        df = pd.read_csv("historical_cyclones.csv")
        df.columns = df.columns.str.strip()  # Clean column names
        return df
    except FileNotFoundError:
        # Using st.error for better visibility in the main app area if the file is critical
        st.error("`historical_cyclones.csv` not found. Historical data feature is disabled.")
        return None    

MODELS = load_all_models()
PERFORMANCE_DF = load_performance_data()    
def send_email_alert(recipient_email, city, model_name, prediction, pressure, wind_speed):
    """Sends an email alert using credentials from st.secrets."""
    try:
        # Get credentials from secrets
        sender_email = st.secrets["SENDER_EMAIL"]
        sender_password = st.secrets["SENDER_PASSWORD"]

        # --- Create the email content ---
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Cyclone Alert for {city}!"

        body = f"""
        <html>
        <body>
            <h2 style="color: #c0392b;">High Severity Cyclone Alert</h2>
            <p>This is an automated alert from the Cyclone Prediction System.</p>
            <p>A prediction using the <b>{model_name}</b> model indicates a potential <b>'{prediction}'</b> severity cyclone for the <b>{city}</b> area.</p>
            
            <h4>Prediction Details:</h4>
            <ul>
                <li><b>Minimum Pressure:</b> {pressure} hPa</li>
                <li><b>Moderate Wind Speed:</b> {wind_speed} km/h</li>
            </ul>
            
            <p>Please take necessary safety precautions and stay tuned to official announcements.</p>
            <p>Stay Safe!</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        # --- Send the email ---
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        return True # Success
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False # Failure             
@st.cache_data
def load_historical_data():
    """Loads historical cyclone data from a CSV file."""
    try:
        df = pd.read_csv("historical_cyclones.csv")
        df.columns = df.columns.str.strip()  # Clean column names
        return df
    except FileNotFoundError:
        st.sidebar.error("`historical_cyclones.csv` not found. Historical data feature is disabled.")
        return None

# --- Application Data ---
MODELS = load_all_models()
PERFORMANCE_DF = load_performance_data()
HISTORICAL_DF = load_historical_data() 
CITY_DATA = {
    "Chennai": (13.0674, 80.2376), "Mumbai": (19.0761, 72.8774), "Kolkata": (22.5726, 88.3639),
    "Visakhapatnam": (17.7041, 83.2977), "Kakinada": (16.93, 82.23), "Karaikal": (10.9254, 79.8380),
    "Tuticorin": (8.7642, 78.1348), "Nagapattinam": (10.7668, 79.8436), "Puducherry": (11.9139, 79.8145),
    "Surat":(21.1702,72.8311), "Porbandar":(21.6417,69.6293), "Veraval":(20.9077,70.3679),
    "Ratnagiri":(16.9944,73.3007), "Karwar":(14.8136,74.1297), "Panaji":(15.4909,73.8278),
    "Alappuzha":(9.4981,76.3388), "Kollam":(8.8932,76.6141), "Cuddalore":(11.7447,79.7680),
    "Diu":(20.7144,70.9870), "Jamnagar":(22.4707,70.0577), "Mandapam":(9.2795,79.1213)
}
API_KEY = "a93a426093ba976321864b03434d075d"

# -------------------------------------------------------------------
# 3. UI LAYOUT
# -------------------------------------------------------------------
st.title("🌪️ Comparative Analysis of ML & DL Techniques for Cyclone Prediction")
# --- Create the Tabs ---
tab1, tab2, tab3,tab4 = st.tabs(["🌪️ Prediction Dashboard", "📊 Analysis Charts","🔬 Model Comparison", "📜 Historical Data"])

# --- Tab 1: Prediction Dashboard (The main page) ---
with tab1:
    col_main_1, col_main_2 = st.columns([1, 1])  # Main columns for the dashboard

    with col_main_1:
        st.subheader("🤖 Select Prediction Model")
        selected_model_name = st.selectbox("Choose an algorithm:", list(MODELS.keys()))
        
        st.subheader("📍 City Selection")
        city = st.selectbox("Select Coastal City", list(CITY_DATA.keys()), label_visibility="collapsed")
        latitude, longitude = CITY_DATA[city]
        st.write(f"Displaying map for **{city}** (Lat: {latitude}, Lon: {longitude})")
        m = folium.Map(location=[latitude, longitude], zoom_start=8)
        folium.Marker([latitude, longitude], popup=city, tooltip=city).add_to(m)
        st_folium(m, height=450)

    with col_main_2:
        st.subheader("🌦️ Weather Data Source")
        data_source = st.radio("Choose an option:", ('Manual Input', 'Fetch Current', 'Fetch 24-Hour Forecast'), horizontal=True)
        
        pressure, wind_speed = 1000, 50  # Default values
        
        # --- API Data Fetching Logic ---
        if data_source == 'Fetch Current':
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                res = requests.get(url).json()
                if res["cod"] == 200:
                    pressure = res["main"]["pressure"]
                    wind_speed = res["wind"]["speed"] * 3.6
                    st.success("✅ Current weather data loaded!")
                else: st.error(f"⚠️ Error: {res['message']}")
            except Exception as e: st.error(f"⚠️ Network error: {e}")
        
        elif data_source == 'Fetch 24-Hour Forecast':
            try:
                url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
                res = requests.get(url).json()
                if res["cod"] == "200":
                    
                  
                    with st.expander("📈 Click to view 24-Hour Forecast Details", expanded=True):
                        forecast_data = [{"Time": pd.to_datetime(i['dt_txt']), "Pressure (hPa)": i['main']['pressure'], "Wind Speed (km/h)": i['wind']['speed'] * 3.6} for i in res['list'][:8]]
                        forecast_df = pd.DataFrame(forecast_data).set_index("Time")
                        st.line_chart(forecast_df)
                        
                        time_options = {f"{t.strftime('%b %d, %H:%M')} (P: {p:.0f}, W: {w:.0f})": t for t, p, w in zip(forecast_df.index, forecast_df['Pressure (hPa)'], forecast_df['Wind Speed (km/h)'])}
                        selected_time_str = st.selectbox("Select a forecast time to use for prediction:", list(time_options.keys()))
                        if selected_time_str:
                            selected_time = time_options[selected_time_str]
                            pressure = forecast_df.loc[selected_time]['Pressure (hPa)']
                            wind_speed = forecast_df.loc[selected_time]['Wind Speed (km/h)']
      

                else: st.error(f"⚠️ Error: {res['message']}")
            except Exception as e: st.error(f"⚠️ Network error: {e}")

        # --- Sliders for all parameters ---
        st.subheader("🌬️ Adjust Parameters")
        min_pressure = st.slider("Minimum Pressure (hPa)", 900, 1100, int(pressure))
        low_wind = st.slider("Low Wind Speed (km/h)", 0, 100, int(wind_speed * 0.6))
        moderate_wind = st.slider("Moderate Wind Speed (km/h)", 0, 200, int(wind_speed))
        high_wind = st.slider("High Wind Speed (km/h)", 0, 300, int(wind_speed * 1.5))
        # --- Email Alert Input ---
        st.markdown("---")
        st.subheader("📧 Get an Email Alert")
        recipient_email = st.text_input("Enter your email for a high severity alert:", placeholder="example@email.com")
        
        # --- Prediction Button and Logic ---
        if st.button("🔍 Predict Cyclone Severity", use_container_width=True, type="primary"):
            model_to_use = MODELS[selected_model_name]
            if model_to_use:
                input_df = pd.DataFrame([{"Latitude": latitude, "Longitude": longitude, "Minimum Pressure": min_pressure, "Total_Low_Wind": low_wind, "Total_Moderate_Wind": moderate_wind, "Total_High_Wind": high_wind}])
                required_cols = ['Latitude', 'Longitude', 'Minimum Pressure', 'Total_Low_Wind', 'Total_Moderate_Wind', 'Total_High_Wind']
                
                prediction_encoded = model_to_use.predict(input_df[required_cols])[0]
                prediction_label = LABEL_ENCODER.inverse_transform([prediction_encoded])[0]

                st.success(f"Predicted Severity (using {selected_model_name}): **{prediction_label}**")
                
                if prediction_label == "High" and recipient_email:
                    with st.spinner("Sending high severity alert via email..."):
                        if send_email_alert(recipient_email, city, selected_model_name, prediction_label, min_pressure, moderate_wind):
                            st.info(f"✅ High severity alert successfully sent to {recipient_email}")
                elif prediction_label == "High" and not recipient_email:
                    st.warning("Prediction is 'High' severity. Enter an email address to receive an alert.")


    st.markdown("---")
    st.subheader("Live Gauges")
    col_gauge_1, col_gauge_2 = st.columns(2)
    with col_gauge_1:
        fig_wind = go.Figure(go.Indicator(mode="gauge+number", value=moderate_wind, title={'text': "Moderate Wind (km/h)"}, gauge={'axis': {'range': [None, 250]}, 'bar': {'color': "royalblue"}, 'steps': [{'range': [0, 80], 'color': "lightgreen"}, {'range': [80, 150], 'color': "yellow"}, {'range': [150, 250], 'color': "red"}]}))
        st.plotly_chart(fig_wind, use_container_width=True)
    with col_gauge_2:
        fig_pressure = go.Figure(go.Indicator(mode="gauge+number", value=min_pressure, title={'text': "Pressure (hPa)"}, gauge={'axis': {'range': [900, 1050]}, 'bar': {'color': "darkblue"}, 'steps': [{'range': [900, 960], 'color': "red"}, {'range': [960, 1000], 'color': "yellow"}, {'range': [1000, 1050], 'color': "lightgreen"}]}))
        st.plotly_chart(fig_pressure, use_container_width=True)

# --- Tab 2: Analysis Charts ---
with tab2:
    st.header("📊 Meteorological Analysis for Selected Parameters")
    st.info(f"Charts below are based on the parameters set in the 'Prediction Dashboard' tab: **{min_pressure} hPa** and **{moderate_wind} km/h**.")
    col_chart_1, col_chart_2 = st.columns(2)
    with col_chart_1:
        st.subheader("Pressure vs Severity")
        pressure_data = pd.DataFrame({'General Trend': [1, 2, 3, 4, 5, 6]}, index=[1010, 1000, 990, 970, 950, 920])
        pressure_data['Your Selection'] = 0
        closest_pressure_index = (pressure_data.index.to_series() - min_pressure).abs().idxmin()
        pressure_data.loc[closest_pressure_index, 'Your Selection'] = pressure_data.loc[closest_pressure_index, 'General Trend']
        st.bar_chart(pressure_data)
        st.caption("Lower pressure correlates with higher severity.")
    with col_chart_2:
        st.subheader("Wind Speed vs Severity")
        wind_data = pd.DataFrame({'General Trend': [1, 2, 3, 4, 5]}, index=[50, 100, 150, 200, 250])
        wind_data['Your Selection'] = 0
        closest_wind_index = (wind_data.index.to_series() - moderate_wind).abs().idxmin()
        wind_data.loc[closest_wind_index, 'Your Selection'] = wind_data.loc[closest_wind_index, 'General Trend']
        st.bar_chart(wind_data)
        st.caption("Higher wind speed correlates with higher severity.")
        
with tab3:
    st.header("🔬 Comparative Performance of Models")
    if PERFORMANCE_DF is not None:
        st.dataframe(PERFORMANCE_DF.style.highlight_max(axis=0, color='lightgreen'))
    else:
        st.warning("Performance data file (`model_performance.json`) not found.")        

# --- Tab 4: Historical Data ---
with tab4:
    st.header(f"📜 Past Cyclone History for {city}")
    if HISTORICAL_DF is not None:
        city_history_df = HISTORICAL_DF[HISTORICAL_DF['City'].str.strip() == city]
        if not city_history_df.empty:
            st.dataframe(city_history_df[['Year', 'CycloneName', 'Severity', 'WindSpeed_kmh']], use_container_width=True, hide_index=True)
        else:
            st.info(f"No historical data available for **{city}** in our records.")
    else:
        st.warning("Historical data file could not be loaded.")

# --- Footer ---
st.markdown("---")
st.caption("Developed by Viki • Infosystem Thanjavur")