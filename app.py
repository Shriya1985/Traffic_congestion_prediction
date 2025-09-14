import pandas as pd
import streamlit as st

# Load processed traffic data
df = pd.read_csv("Processed_Traffic_Data.csv")

st.set_page_config(page_title="Traffic Congestion Predictor", layout="wide")

st.title("🚦 Traffic Congestion Predictor")
st.markdown("### Analyze and predict expected traffic levels by time of day")

# User input controls
col1, col2, col3 = st.columns(3)
with col1:
    hour = st.slider("Select Hour of Day", 0, 23, 8)
with col2:
    day = st.selectbox("Select Day of Week", sorted(df['day_of_week'].unique()))
with col3:
    month = st.selectbox("Select Month", sorted(df['month'].unique()))

# Filter data
filtered = df[(df['hour'] == hour) & 
              (df['day_of_week'] == day) & 
              (df['month'] == month)]

# Display prediction
st.subheader("Predicted Traffic Level")
if not filtered.empty:
    traffic_level = filtered['traffic_level'].mode()[0]
    avg_volume = int(filtered['traffic_volume'].mean())
    
    if traffic_level == "Low":
        st.success(f"✅ Expected Traffic: {traffic_level} ({avg_volume} vehicles)")
    elif traffic_level == "Medium":
        st.warning(f"⚠️ Expected Traffic: {traffic_level} ({avg_volume} vehicles)")
    else:
        st.error(f"🚨 Expected Traffic: {traffic_level} ({avg_volume} vehicles)")
else:
    st.warning("No data available for this selection.")

# --- Extra Visualizations ---
st.markdown("---")

# Hourly trend for selected day
st.subheader(f"Hourly Traffic Trend on {day}")
trend = df[df['day_of_week'] == day].groupby('hour')['traffic_volume'].mean()
st.line_chart(trend)


