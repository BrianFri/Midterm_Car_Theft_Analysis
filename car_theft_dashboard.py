import os
from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="U.S. Car Theft Dashboard - 2025",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- HEADER ----------------
st.title("U.S. Car Theft Analysis Dashboard")
st.markdown("**2025 Data** - Analysis of vehicle thefts and popularity by state")


# ---------------- DATA LOADING ----------------
@st.cache_data
def load_car_data(
    file_path="Data/2025_State_Top10Report_wTotalThefts.csv",
):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        uploaded_file = st.file_uploader(
            "Upload 2025_State_Top10Report_wTotalThefts.csv", type=["csv"]
        )
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
        else:
            st.warning("Please upload the CSV or place it in the Data folder.")
            st.stop()

    df["Thefts"] = pd.to_numeric(
        df["Thefts"].astype(str).str.replace(",", ""), errors="coerce"
    ).fillna(0)
    df = df.dropna(subset=["State"])
    df["State"] = df["State"].astype(str).str.strip().str.title()
    return df


car_df = load_car_data()

# ---------------- 2025 POPULATION ----------------
population = {
    "Alabama": 5193088,
    "Alaska": 737270,
    "Arizona": 7623818,
    "Arkansas": 3114791,
    "California": 39355309,
    "Colorado": 6012561,
    "Connecticut": 3688496,
    "Delaware": 1059952,
    "Florida": 23462518,
    "Georgia": 11302748,
    "Hawaii": 1432820,
    "Idaho": 2029733,
    "Illinois": 12719141,
    "Indiana": 6973333,
    "Iowa": 3238387,
    "Kansas": 2977220,
    "Kentucky": 4606864,
    "Louisiana": 4618189,
    "Maine": 1414874,
    "Maryland": 6265347,
    "Massachusetts": 7154084,
    "Michigan": 10127884,
    "Minnesota": 5830405,
    "Mississippi": 2954160,
    "Missouri": 6270541,
    "Montana": 1144694,
    "Nebraska": 2018006,
    "Nevada": 3282188,
    "New Hampshire": 1415342,
    "New Jersey": 9548215,
    "New Mexico": 2125498,
    "New York": 20002427,
    "North Carolina": 11197968,
    "North Dakota": 799358,
    "Ohio": 11900510,
    "Oklahoma": 4123288,
    "Oregon": 4273586,
    "Pennsylvania": 13059432,
    "Rhode Island": 1114521,
    "South Carolina": 5570274,
    "South Dakota": 935094,
    "Tennessee": 7315076,
    "Texas": 31709821,
    "Utah": 3538904,
    "Vermont": 644663,
    "Virginia": 8880107,
    "Washington": 8001020,
    "West Virginia": 1766147,
    "Wisconsin": 5972787,
    "Wyoming": 588753,
    "District of Columbia": 693645,
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

# ---------------- MOST POPULAR 2025 ----------------
most_popular_2025 = {
    "Alabama": "Ford F-150",
    "Alaska": "Toyota RAV4",
    "Arizona": "Ford F-150",
    "Arkansas": "Ford F-150",
    "California": "Tesla Model Y",
    "Colorado": "Toyota RAV4",
    "Connecticut": "Honda CR-V",
    "Delaware": "Toyota RAV4",
    "District of Columbia": "Honda CR-V",
    "Florida": "Ford F-150",
    "Georgia": "Ford F-150",
    "Hawaii": "Toyota RAV4",
    "Idaho": "Ford F-150",
    "Illinois": "Chevrolet Silverado 1500",
    "Indiana": "Ford F-150",
    "Iowa": "Ford F-150",
    "Kansas": "Ford F-150",
    "Kentucky": "Ford F-150",
    "Louisiana": "Ford F-150",
    "Maine": "Toyota RAV4",
    "Maryland": "Honda CR-V",
    "Massachusetts": "Toyota RAV4",
    "Michigan": "Ford F-150",
    "Minnesota": "Toyota RAV4",
    "Mississippi": "Ford F-150",
    "Missouri": "Ford F-150",
    "Montana": "Ford F-150",
    "Nebraska": "Ford F-150",
    "Nevada": "Tesla Model Y",
    "New Hampshire": "Toyota RAV4",
    "New Jersey": "Honda CR-V",
    "New Mexico": "Ford F-150",
    "New York": "Honda CR-V",
    "North Carolina": "Ford F-150",
    "North Dakota": "Ford F-150",
    "Ohio": "Ford F-150",
    "Oklahoma": "Ford F-150",
    "Oregon": "Toyota RAV4",
    "Pennsylvania": "Ford F-150",
    "Rhode Island": "Honda CR-V",
    "South Carolina": "Ford F-150",
    "South Dakota": "Ford F-150",
    "Tennessee": "Ford F-150",
    "Texas": "Ford F-150",
    "Utah": "Toyota RAV4",
    "Vermont": "Toyota RAV4",
    "Virginia": "Ford F-150",
    "Washington": "Toyota RAV4",
    "West Virginia": "Ford F-150",
    "Wisconsin": "Ford F-150",
    "Wyoming": "Ford F-150",
}

top_25_2025 = [
    ("Ford F-Series", "Truck", 828832),
    ("Chevrolet Silverado", "Truck", 588709),
    ("Toyota RAV4", "SUV", 479288),
    ("Honda CR-V", "SUV", 403768),
    ("Ram Pickup", "Truck", 374059),
    ("GMC Sierra", "Truck", 356218),
    ("Chevrolet Equinox", "SUV", 332301),
    ("Toyota Camry", "Sedan", 316185),
    ("Tesla Model Y", "SUV (EV)", 317800),
    ("Toyota Tacoma", "Truck", 274638),
    ("Ford Explorer", "SUV", 223000),
    ("Nissan Rogue", "SUV", 218000),
    ("Hyundai Tucson", "SUV", 234000),
    ("Honda Civic", "Sedan", 239000),
    ("Toyota Corolla", "Sedan", 248000),
    ("Jeep Grand Cherokee", "SUV", 210000),
    ("Chevrolet Trax", "SUV", 206000),
    ("Subaru Crosstrek", "SUV", 192000),
    ("Kia Sportage", "SUV", 183000),
    ("Subaru Forester", "SUV", 175000),
    ("Tesla Model 3", "Sedan (EV)", 173000),
    ("Jeep Wrangler", "SUV", 167000),
    ("Subaru Outback", "Wagon/SUV", 158000),
    ("Ford Transit", "Van", 157000),
    ("Ford Maverick", "Truck", 155000),
]

# ---------------- PROCESS DATA ----------------
thefts_by_state = (
    car_df.groupby("State")["Thefts"]
    .sum()
    .reset_index()
    .sort_values("Thefts", ascending=False)
)

thefts_rate = thefts_by_state.merge(
    pd.DataFrame(population.items(), columns=["State", "Population"]), on="State"
)
thefts_rate["Thefts_per_100k"] = (
    thefts_rate["Thefts"] / thefts_rate["Population"] * 100000
).round(2)
thefts_rate["State_Code"] = thefts_rate["State"].map(STATE_CODE)
thefts_rate = thefts_rate.sort_values("Thefts_per_100k", ascending=False)

most_stolen_model = (
    car_df.groupby("Make/Model")["Thefts"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

most_stolen_by_state = car_df.loc[car_df.groupby("State")["Thefts"].idxmax()][
    ["State", "Make/Model", "Thefts"]
].sort_values("State")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Controls")
selected_state = st.sidebar.selectbox(
    "Deep Dive into a State", ["All States"] + sorted(car_df["State"].unique())
)

# ---------------- METRICS ----------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Thefts", f"{thefts_by_state['Thefts'].sum():,.0f}")
col2.metric("Highest Rate State", thefts_rate.iloc[0]["State"])
col3.metric("Highest Rate /100k", f"{thefts_rate.iloc[0]['Thefts_per_100k']:.1f}")
col4.metric("Most Stolen Model", most_stolen_model.iloc[0]["Make/Model"])

st.markdown("---")

# ---------------- TABS ----------------
tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(
    [
        "Introduction",
        "State Theft Totals",
        "Theft Rate per 100k",
        "Top 25 Most Popular Vehicles",
        "Most Stolen Vehicles Nationwide",
        "Popular vs Stolen (National)",
        "Most Popular by State",
        "Most Stolen by State",
        "Popular vs Stolen by State",
        "Least Stolen Among Top 25 by State",
        "What We Learned",
    ]
)
# tab0
with tab0:
    st.header("Introduction")

    st.markdown("""
    - **Which state has the most car thefts?**  
    """)

    st.markdown("""
    - **What is the most stolen vehicle nationally?**  
    """)

    st.markdown("""
    - **Which vehicle is the most stolen across the states?**  
    """)
# Tab 1
with tab1:
    st.header("Total Car Thefts by State (2025)")
    st.dataframe(thefts_by_state.head(15), use_container_width=True, hide_index=True)
    fig = px.bar(
        thefts_by_state.head(15),
        x="State",
        y="Thefts",
        color="Thefts",
        color_continuous_scale="YlOrRd",
    )
    st.plotly_chart(fig, use_container_width=True)

# Tab 2
with tab2:
    st.header("Theft Rate per 100,000 Residents (2025)")
    st.dataframe(
        thefts_rate[["State", "Thefts", "Population", "Thefts_per_100k"]],
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
    )
    st.plotly_chart(fig, use_container_width=True)

# Tab 3
with tab3:
    st.header("Top 25 Most Popular Vehicles in the US (2025)")
    st.caption("Based on new vehicle sales/registrations")

    top25_df = pd.DataFrame(top_25_2025, columns=["Vehicle", "Type", "Sales 2025"])
    st.dataframe(top25_df, use_container_width=True, hide_index=True)

    fig = px.bar(
        top25_df,
        x="Sales 2025",
        y="Vehicle",
        orientation="h",
        title="Top 25 Best-Selling Vehicles in America (2025)",
        color="Sales 2025",
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        height=750,
    )
    st.plotly_chart(fig, use_container_width=True)

# Tab 4
with tab4:
    st.header("Most Stolen Vehicles Nationwide (2025)")
    st.dataframe(most_stolen_model, use_container_width=True, hide_index=True)

# Tab 5
with tab5:
    st.header("Popular vs Stolen Vehicles (National Top 10)")
    st.caption("2025 Comparison")

    stolen_top = most_stolen_model.head(10).copy()
    stolen_top.columns = ["Vehicle", "Thefts"]
    stolen_top.insert(0, "Rank", range(1, 11))

    popular_top = pd.DataFrame(top_25_2025, columns=["Vehicle", "Type", "Sales"]).head(
        10
    )
    popular_top.insert(0, "Rank", range(1, 11))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 Most Popular")
        st.dataframe(
            popular_top[["Rank", "Vehicle", "Type", "Sales"]],
            use_container_width=True,
            hide_index=True,
        )
    with col2:
        st.subheader("Top 10 Most Stolen")
        st.dataframe(
            stolen_top[["Rank", "Vehicle", "Thefts"]],
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("---")
    st.subheader("Vehicles That Appear in Both Lists")
    common = pd.merge(
        popular_top[["Vehicle", "Sales"]],
        stolen_top[["Vehicle", "Thefts"]],
        on="Vehicle",
        how="inner",
    )
    if not common.empty:
        st.dataframe(common, use_container_width=True, hide_index=True)
    else:
        st.info("No overlap between the current top 10 lists.")

# Tab 6
with tab6:
    st.header("Most Popular Vehicle by State (2025)")
    st.caption("Based on new vehicle registration trends")
    popular_df = pd.DataFrame(
        list(most_popular_2025.items()), columns=["State", "Most Popular Vehicle"]
    ).sort_values("State")
    st.dataframe(popular_df, use_container_width=True, hide_index=True)

    st.markdown("**Summary**")
    for vehicle, count in Counter(most_popular_2025.values()).most_common():
        st.write(f"• **{vehicle}** — most popular in **{count}** states")

# Tab 7
with tab7:
    st.header("Most Stolen Vehicle by State (2025)")
    st.dataframe(most_stolen_by_state, use_container_width=True, hide_index=True)

    st.markdown("**Summary**")
    stolen_counts = Counter(most_stolen_by_state["Make/Model"])

    for vehicle, count in stolen_counts.most_common():
        if count >= 3:
            st.write(f"• **{vehicle}** — most stolen in **{count}** states")

with tab8:
    st.header("Popular vs Stolen Vehicle by State (2025)")
    st.caption("Side-by-side comparison per state (50 states + DC)")

    popular_df = pd.DataFrame(
        list(most_popular_2025.items()), columns=["State", "Most Popular Vehicle"]
    )

    stolen_df = most_stolen_by_state.copy()
    non_state_cols = [
        col for col in stolen_df.columns if col.lower().strip() != "state"
    ]

    if len(non_state_cols) == 0:
        st.error("Could not find a vehicle column in most_stolen_by_state.")
        st.stop()

    vehicle_col_name = non_state_cols[0]
    stolen_df = stolen_df.rename(columns={vehicle_col_name: "Most Stolen Vehicle"})[
        ["State", "Most Stolen Vehicle"]
    ]

    # Use inner merge so we only keep the 51 locations from most_popular_2025
    comparison_df = pd.merge(
        popular_df, stolen_df, on="State", how="inner"
    ).sort_values("State")

    comparison_df["Same Vehicle?"] = comparison_df.apply(
        lambda row: "✅ Yes"
        if str(row["Most Popular Vehicle"]).strip().lower()
        == str(row["Most Stolen Vehicle"]).strip().lower()
        else "❌ No",
        axis=1,
    )

    comparison_df = comparison_df[
        ["State", "Most Popular Vehicle", "Most Stolen Vehicle", "Same Vehicle?"]
    ]

    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    st.markdown("### Key Insights")
    same_count = (comparison_df["Same Vehicle?"] == "✅ Yes").sum()
    total = len(comparison_df)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("States Where Popular = Stolen", f"{same_count} / {total}")
    with col2:
        st.metric("States With Different Vehicles", f"{total - same_count} / {total}")

    if same_count > 0:
        st.markdown(
            "#### Vehicles That Are Both Most Popular & Most Stolen in the Same State"
        )
        both = comparison_df[comparison_df["Same Vehicle?"] == "✅ Yes"][
            "Most Popular Vehicle"
        ].value_counts()
        for vehicle, count in both.items():
            st.write(f"• **{vehicle}** in **{count}** state(s)")
# Tab 9
with tab9:
    st.header("Least Stolen Vehicle Among Top 25 by State (2025)")
    st.caption(
        "Out of the 25 most stolen vehicles nationally, which one has the fewest thefts in each state?"
    )

    top_25_vehicles = (
        car_df.groupby("Make/Model")["Thefts"].sum().nlargest(25).index.tolist()
    )
    filtered_df = car_df[car_df["Make/Model"].isin(top_25_vehicles)]

    least_stolen_top25 = (
        filtered_df.loc[filtered_df.groupby("State")["Thefts"].idxmin()][
            ["State", "Make/Model", "Thefts"]
        ]
        .sort_values("State")
        .reset_index(drop=True)
    )

    st.dataframe(least_stolen_top25, use_container_width=True, hide_index=True)

with tab10:
    st.markdown("### Key Takeaways")

    st.markdown("""
    - **California** has the highest total number of vehicle thefts in the country by a significant margin.

    - The **RAM 1500** is the most stolen vehicle nationally, followed closely by Honda and other high-volume models. Many of the top stolen vehicles are also among the most commonly sold cars.

    - The most popular cars does not corilate with the most stolen cars

    """)

    st.markdown("---")
    st.markdown("""
    ### Final Thought
    This analysis shows that **vehicle theft is not random**, it follows clear patterns based on mostly location.
    """)

# ---------------- DEEP DIVE ----------------
if selected_state != "All States":
    st.markdown("---")
    st.header(f"Deep Dive: {selected_state}")

    state_data = car_df[car_df["State"] == selected_state].sort_values(
        "Thefts", ascending=False
    )

    total_thefts = state_data["Thefts"].sum()
    top_vehicle_row = state_data.iloc[0]
    top_vehicle = top_vehicle_row["Make/Model"]
    top_vehicle_thefts = top_vehicle_row["Thefts"]

    recommended_vehicle = most_popular_2025.get(selected_state, "N/A")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Thefts", f"{total_thefts:,.0f}")
    col2.metric("Most Stolen Vehicle", top_vehicle)
    col3.metric("Thefts of Top Vehicle", f"{top_vehicle_thefts:,}")

    st.markdown("---")

    # Top stolen vehicles table
    st.subheader(f"Top Stolen Vehicles in {selected_state}")
    st.dataframe(
        state_data[["Make/Model", "Model Year", "Thefts"]].head(15),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    percentage = top_vehicle_thefts / total_thefts * 100

    st.markdown(
        f"""
        <div style="
            background-color: #1f2a40; 
            padding: 20px; 
            border-radius: 12px; 
            border-left: 5px solid #4ade80;
            margin-top: 10px;
        ">
            <p style="margin: 0; font-size: 1.05rem; color: #e2e8f0;">
                <strong>{top_vehicle}</strong> accounts for <strong>{percentage:.1f}%</strong> of all thefts in {selected_state}.
            </p>
            <p style="margin: 12px 0 0 0; font-size: 1.25rem; font-weight: 700; color: #4ade80;">
                Recommended Vehicle: {recommended_vehicle}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
