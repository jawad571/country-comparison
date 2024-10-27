import streamlit as st
import pandas as pd

# Define data for each country
countries_data = {
    "Pakistan": {"GDP": 376.5, "Unemployment": 6.3, "Inflation": 27.4},
    "India": {"GDP": 3290.0, "Unemployment": 7.2, "Inflation": 5.6},
    "Malaysia": {"GDP": 434.0, "Unemployment": 3.7, "Inflation": 2.8},
    "Kazakhstan": {"GDP": 237.0, "Unemployment": 4.9, "Inflation": 15.0},
    "Bangladesh": {"GDP": 460.8, "Unemployment": 5.3, "Inflation": 8.0},
    "Croatia": {"GDP": 71.0, "Unemployment": 6.0, "Inflation": 7.3}
}

# Define score ranges for each metric
score_ranges = {
    "GDP": [(0, 100, 1), (100, 500, 2), (500, 1000, 3), (1000, 3000, 4), (3000, float('inf'), 5)],
    "Unemployment": [(0, 3, 5), (3, 5, 4), (5, 7, 3), (7, 10, 2), (10, float('inf'), 1)],
    "Inflation": [(0, 2, 5), (2, 4, 4), (4, 6, 3), (6, 10, 2), (10, float('inf'), 1)]
}

# Function to assign score based on ranges
def get_score(metric, value):
    for lower, upper, score in score_ranges[metric]:
        if lower <= value < upper:
            return score
    return 0

# Streamlit interface
st.header("Step 1: Input Countries you want to compare")
options = st.multiselect(
    "Choose the countries",
    ["Pakistan", "India", "Bangladesh", "Kazakhstan", "Malaysia", "Croatia"],
    []
)


st.header("Step 2: Assign Weightage to each Criterion")
GDP_weight = st.number_input("Input Weightage for GDP", value=0.45, min_value=0.0, max_value=1.0, step=0.01)
UNEMPLOYMENT_weight = st.number_input("Input Weightage for UNEMPLOYMENT", value=0.45, min_value=0.0, max_value=1.0, step=0.01)
INFLATION_weight = st.number_input("Input Weightage for INFLATION", value=0.10, min_value=0.0, max_value=1.0, step=0.01)

# Check if the total weightage is valid
total_weight = GDP_weight + UNEMPLOYMENT_weight + INFLATION_weight
if total_weight > 1:
    st.warning("Total weightage exceeds 1. Please adjust the values so the sum of all weightages is 1 or less.")
else:
    # Calculate weighted score for each selected country
    if options:
        st.header("Country Scores", divider=True)
        for country in options:
            gdp_score = get_score("GDP", countries_data[country]["GDP"]) * GDP_weight
            unemployment_score = get_score("Unemployment", countries_data[country]["Unemployment"]) * UNEMPLOYMENT_weight
            inflation_score = get_score("Inflation", countries_data[country]["Inflation"]) * INFLATION_weight

            # Calculate total weighted score
            total_score = gdp_score + unemployment_score + inflation_score

            # Display the result
            st.write(f"**{country}**: Total Score = {total_score:.2f}")

col1, col2 = st.columns(2)
# Convert score_ranges to a DataFrame for display
score_ranges_df = pd.DataFrame({
    "Metric": ["GDP", "GDP", "GDP", "GDP", "GDP", "Unemployment", "Unemployment", "Unemployment", "Unemployment", "Unemployment", "Inflation", "Inflation", "Inflation", "Inflation", "Inflation"],
    "Range": [
        "0-100", "100-500", "500-1000", "1000-3000", "3000+", 
        "0-3", "3-5", "5-7", "7-10", "10+",
        "0-2", "2-4", "4-6", "6-10", "10+"
    ],
    "Score": [1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 5, 4, 3, 2, 1]
})

# Convert countries_data to a DataFrame for display
countries_data_df = pd.DataFrame(countries_data).T
countries_data_df.columns = ["GDP (billion USD)", "Unemployment (%)", "Inflation (%)"]

with col1:
    # Display tables
    st.header("Score Ranges")
    st.table(score_ranges_df)

with col2:
    st.header("Countries Data")
    st.table(countries_data_df)

    