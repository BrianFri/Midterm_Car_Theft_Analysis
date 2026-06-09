import os

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Car Theft Dashboard", layout="wide")

st.title("U.S. Car Theft Analysis")


@st.cache_data
def load_car_data(
    file_path: str = "Data/2015_State_Top10Report_wTotalThefts.csv",
) -> pd.DataFrame:
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
        else:
            st.warning("Please upload the CSV file or place it in the Data/ folder.")
            st.stop()

    df["Thefts"] = pd.to_numeric(
        df["Thefts"].astype(str).str.replace(",", ""), errors="coerce"
    ).fillna(0)

    # Clean State names (this is the key fix)
    df = df.dropna(subset=["State"])
    df["State"] = df["State"].astype(str).str.strip().str.title()

    return df


# total thefts by state.
def get_thefts_by_state(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("State")["Thefts"]
        .sum()
        .reset_index()
        .sort_values("Thefts", ascending=False)
    )


# Calculate thefts per 100k residents.
def get_theft_rates(thefts_by_state: pd.DataFrame, population: dict) -> pd.DataFrame:
    pop_df = pd.DataFrame(population.items(), columns=["State", "Population"])

    # Clean population state names too
    pop_df["State"] = pop_df["State"].str.strip().str.title()

    # Use inner join so we only keep states that have population data
    rates = thefts_by_state.merge(pop_df, on="State", how="inner")

    rates["Thefts_per_100k"] = (rates["Thefts"] / rates["Population"] * 100_000).round(
        2
    )

    rates = rates.sort_values("Thefts_per_100k", ascending=False)
    return rates


# Most stolen vehicles by model (all years combined).
def get_most_stolen_overall(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Make/Model")["Thefts"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


# Most stolen vehicle in each state.
def get_most_stolen_by_state(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.loc[df.groupby("State")["Thefts"].idxmax()][
            ["State", "Make/Model", "Thefts"]
        ]
        .sort_values("State")
        .reset_index(drop=True)
    )


# Least stolen vehicle in each state.
def get_least_stolen_by_state(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.loc[df.groupby("State")["Thefts"].idxmin()][
            ["State", "Make/Model", "Thefts"]
        ]
        .sort_values("State")
        .reset_index(drop=True)
    )


car_df = load_car_data()

population = {
    "Alabama": 4858979,
    "Alaska": 738432,
    "Arizona": 6828065,
    "Arkansas": 2978204,
    "California": 39144818,
    "Colorado": 5456574,
    "Connecticut": 3590886,
    "Delaware": 945934,
    "Florida": 20271272,
    "Georgia": 10214860,
    "Hawaii": 1431603,
    "Idaho": 1654930,
    "Illinois": 12859995,
    "Indiana": 6619680,
    "Iowa": 3123899,
    "Kansas": 2911505,
    "Kentucky": 4425092,
    "Louisiana": 4670724,
    "Maine": 1329328,
    "Maryland": 6006401,
    "Massachusetts": 6794422,
    "Michigan": 9922576,
    "Minnesota": 5489594,
    "Mississippi": 2992333,
    "Missouri": 6083672,
    "Montana": 1032949,
    "Nebraska": 1896190,
    "Nevada": 2890845,
    "New Hampshire": 1330608,
    "New Jersey": 8958013,
    "New Mexico": 2085109,
    "New York": 19795791,
    "North Carolina": 10042802,
    "North Dakota": 756927,
    "Ohio": 11613423,
    "Oklahoma": 3911338,
    "Oregon": 4028977,
    "Pennsylvania": 12802503,
    "Rhode Island": 1056298,
    "South Carolina": 4896146,
    "South Dakota": 858469,
    "Tennessee": 6600299,
    "Texas": 27469114,
    "Utah": 2995919,
    "Vermont": 626042,
    "Virginia": 8382993,
    "Washington": 7170351,
    "West Virginia": 1844128,
    "Wisconsin": 5771337,
    "Wyoming": 586107,
    "District of Columbia": 672228,
}

STATE_CODE = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
}

st.set_page_config(page_title="U.S. Car Theft Analysis", layout="wide")
st.title("U.S. Car Theft Analysis Dashboard")

car_df = load_car_data()

# Process data using reusable functions
thefts_by_state = get_thefts_by_state(car_df)
thefts_rate = get_theft_rates(thefts_by_state, population)
thefts_rate["State_Code"] = thefts_rate["State"].map(STATE_CODE)

most_stolen_model = get_most_stolen_overall(car_df)
most_stolen_by_state = get_most_stolen_by_state(car_df)
least_stolen_by_state = get_least_stolen_by_state(car_df)

st.sidebar.header("Controls")
top_n = 10
selected_state = st.sidebar.selectbox(
    "Deep Dive into a State",
    options=["All States"] + sorted(car_df["State"].unique()),
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Reported Thefts", f"{thefts_by_state['Thefts'].sum():,.0f}")
col2.metric("Highest Theft Rate State", thefts_rate.iloc[0]["State"])
col3.metric("Highest Rate (per 100k)", f"{thefts_rate.iloc[0]['Thefts_per_100k']:.1f}")
col4.metric("Most Stolen Model", most_stolen_model.iloc[0]["Make/Model"])

st.markdown("---")

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "State Theft Totals",
        "Theft Rate per 100k",
        "Most Stolen Vehicles",
        "Most Stolen by State",
        "Least Stolen by State",
    ]
)

with tab1:
    st.header("Total Car Thefts by State")
    st.dataframe(thefts_by_state.head(top_n), use_container_width=True, hide_index=True)

    fig = px.bar(
        thefts_by_state.head(top_n),
        x="State",
        y="Thefts",
        title=f"Top {top_n} States by Total Thefts",
        color="Thefts",
        color_continuous_scale="YlOrRd",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Car Theft Rate per 100,000 Residents")
    st.dataframe(
        thefts_rate[["State", "Thefts", "Population", "Thefts_per_100k"]].head(top_n),
        use_container_width=True,
        hide_index=True,
    )

    fig = px.choropleth(
        thefts_rate,
        locations="State_Code",
        locationmode="USA-states",
        color="Thefts_per_100k",
        scope="usa",
        color_continuous_scale="Reds",
        hover_name="State",
        title="Theft Rate per 100,000 Residents",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Most Stolen Vehicles Nationwide")
    st.dataframe(most_stolen_model.head(15), use_container_width=True, hide_index=True)

with tab4:
    st.header("Most Stolen Vehicle by State")
    st.dataframe(
        most_stolen_by_state.head(51), use_container_width=True, hide_index=True
    )

with tab5:
    st.header("Least Stolen Vehicle by State")
    st.dataframe(
        least_stolen_by_state.head(50), use_container_width=True, hide_index=True
    )


# ---------------- STATE DEEP DIVE ----------------
if selected_state != "All States":
    st.markdown("---")
    st.header(f"Deep Dive: {selected_state}")

    state_data = car_df[car_df["State"] == selected_state].sort_values(
        "Thefts", ascending=False
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Top Models in This State")
        st.dataframe(
            state_data[["Rank", "Make/Model", "Model Year", "Thefts"]],
            use_container_width=True,
            hide_index=True,
        )

    with col_b:
        state_rate = thefts_rate[thefts_rate["State"] == selected_state]
        if not state_rate.empty:
            st.metric(
                "Thefts per 100k", f"{state_rate['Thefts_per_100k'].values[0]:.2f}"
            )
            st.metric("Total Thefts", f"{state_rate['Thefts'].values[0]:,.0f}")
            st.metric(
                "Most Stolen Model",
                most_stolen_by_state[most_stolen_by_state["State"] == selected_state][
                    "Make/Model"
                ].values[0],
            )
