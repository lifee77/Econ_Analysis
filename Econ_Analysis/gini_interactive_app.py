import streamlit as st
import pandas as pd
import plotly.express as px

# Load and preprocess the data
@st.cache
def load_data(file_path):
    gini_data = pd.read_csv(file_path, skiprows=4).drop(columns=["Unnamed: 68"]).dropna(how="all", axis=0).reset_index(drop=True)
    gini_long = gini_data.melt(
        id_vars=["Country Name", "Country Code"],
        var_name="Year",
        value_name="Gini Index"
    ).dropna(subset=["Gini Index"])
    gini_long["Year"] = pd.to_numeric(gini_long["Year"], errors="coerce")
    return gini_long

# Load the dataset
file_path = "gini_world_data.csv"  # Update with the correct path
gini_long = load_data(file_path)

# Streamlit UI
st.title("Interactive Gini Index Visualization")
st.sidebar.header("Filters")

# Dropdown for selecting a country
selected_country = st.sidebar.selectbox(
    "Select a country",
    gini_long["Country Name"].unique(),
    index=0
)

# Filter data for the selected country
country_data = gini_long[gini_long["Country Name"] == selected_country]

# Line chart for the selected country
st.subheader(f"Gini Index Trend for {selected_country}")
fig = px.line(country_data, x="Year", y="Gini Index", title=f"{selected_country} Gini Index Over Time")
st.plotly_chart(fig)

# Multiselect for comparing multiple countries
st.sidebar.subheader("Compare Countries")
selected_countries = st.sidebar.multiselect(
    "Select countries to compare",
    gini_long["Country Name"].unique(),
    default=["Nepal", "India"]
)

# Filter data for the selected countries
comparison_data = gini_long[gini_long["Country Name"].isin(selected_countries)]

# Line chart for multiple countries
st.subheader("Comparison of Gini Index Across Countries")
fig_comparison = px.line(
    comparison_data,
    x="Year",
    y="Gini Index",
    color="Country Name",
    title="Comparison of Gini Index Trends"
)
st.plotly_chart(fig_comparison)
