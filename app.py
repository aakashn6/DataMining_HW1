import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
st.title("🚗 NYC Traffic Accidents Dashboard")

# Try loading the dataset with error handling
try:
    df = pd.read_excel("Motor_Vehicle_Collisions_-_Crashes_20250223.xlsx")
except FileNotFoundError:
    st.error("Error: Dataset file not found! Please make sure it's in the correct directory.")
    st.stop()

# Convert "CRASH DATE" to datetime safely
df['CRASH DATE'] = pd.to_datetime(df['CRASH DATE'], errors='coerce')

# Drop rows with missing dates
df = df.dropna(subset=['CRASH DATE'])

# Extract hour from "CRASH TIME" safely
df['HOUR'] = pd.to_datetime(df['CRASH TIME'], errors='coerce').dt.hour

# Borough Selection
boroughs = df["BOROUGH"].dropna().unique()
if len(boroughs) == 0:
    st.warning("No borough data available.")
    st.stop()

borough = st.selectbox("Select Borough:", boroughs)

# Filter data for selected borough
filtered_data = df[df["BOROUGH"] == borough]

# Display total accidents
st.subheader(f"Total Accidents in {borough}: {len(filtered_data)}")

# 📅 Accident Trends Over Time (Line Chart)
st.subheader("📅 Accident Trends Over Time")
if not filtered_data.empty:
    accidents_per_day = filtered_data.groupby(filtered_data['CRASH DATE'].dt.date).size()
    
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(accidents_per_day.index, accidents_per_day.values, color='red', linewidth=2)
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Accidents")
    ax.set_title(f"Daily Trend of Accidents in {borough}")
    st.pyplot(fig)
else:
    st.warning("No accident data available for this borough.")

# ⏰ Accidents by Hour (Histogram)
st.subheader("⏰ Accidents by Hour")
if not filtered_data.empty:
    fig, ax = plt.subplots(figsize=(10,5))
    ax.hist(filtered_data['HOUR'].dropna(), bins=24, color='blue', alpha=0.7, edgecolor='black')
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Number of Accidents")
    ax.set_title(f"Accidents Distribution by Hour in {borough}")
    st.pyplot(fig)
else:
    st.warning("No time data available for this borough.")

# 🔍 Show a sample of the dataset
st.subheader("🔍 Explore the Dataset")
st.dataframe(filtered_data.head(10))
