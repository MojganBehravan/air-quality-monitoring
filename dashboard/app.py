import streamlit as st
import pandas as pd
import requests

st.title("Air Quality Dashboard")

# API endpoints
summary_url = "http://delivery:5000/summary"
filter_url = "http://delivery:5000/filter"
metadata_url = "http://delivery:5000/metadata"

# --- Load metadata for dropdowns ---
try:
    meta_response = requests.get(metadata_url)
    meta_response.raise_for_status()
    metadata = meta_response.json()

    # Convert metadata to dropdown lists
    states = sorted(metadata.get("states", []))
    years = sorted(metadata.get("years", []))

    if not states or not years:
        st.error("States or years are empty. Please check the metadata API.")
        st.stop()

except Exception as e:
    st.error(f"Failed to load metadata: {e}")
    st.stop()

# --- Summary Section ---
summary_response = requests.get(summary_url)
if summary_response.status_code == 200:
    summary_data = summary_response.json()
    df_summary = pd.DataFrame(summary_data)
    df_summary["Date Local"] = pd.to_datetime(df_summary["Date Local"])

    if st.button("Show Summary"):
        st.subheader("Top Records:")
        st.dataframe(df_summary)
else:
    st.error("Failed to load summary data from API.")

# --- Filter Form ---
st.write("### Filter Data")
selected_state = st.selectbox("Select State", states)
selected_year = st.selectbox("Select Year", years)

if st.button("Filter Data"):
    params = {"state": selected_state, "year": str(selected_year)}
    response = requests.get(filter_url, params=params)

    if response.status_code == 200:
        results = response.json()
        if not results:
            st.warning("No data found for the given filters.")
        else:
            df = pd.DataFrame(results)

            required_fields = {"avg_CO", "avg_NO2", "avg_O3", "avg_SO2", "Date Local", "state"}
            if not required_fields.issubset(df.columns):
                st.error("Expected fields not found in the data.")
            else:
                # Convert dates and extract months
                df["Date Local"] = pd.to_datetime(df["Date Local"])
                df["month"] = df["Date Local"].dt.month

                # Group by month and average pollutants
                monthly_avg = df.groupby("month")[["avg_CO", "avg_NO2", "avg_O3", "avg_SO2"]].mean().reset_index()

                # Reshape for plotting
                melted = monthly_avg.melt(id_vars="month", var_name="pollutant", value_name="average")

                st.subheader(f"Monthly Pollution Trends in {selected_state}, {selected_year}")
                st.line_chart(melted.pivot(index="month", columns="pollutant", values="average"))
    else:
        st.error("Failed to fetch data from API.")
