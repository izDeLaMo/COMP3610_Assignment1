"""
NYC Taxi Trip Dashboard - Full Streamlit App
============================================
Displays metrics, interactive charts, and insights from NYC yellow taxi data.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------- Page Setup -----------------------
st.set_page_config(
    page_title="NYC Taxi Dashboard",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚕 NYC Taxi Trip Dashboard")
st.markdown("Explore NYC Yellow Taxi data with interactive charts and key metrics.")

# ----------------------- Load Data -----------------------
@st.cache_data
def load_data():
    parquet_path = "data/raw/yellowtripdata.parquet"
    try:
        df = pd.read_parquet(parquet_path)
    except FileNotFoundError:
        st.error(f"Dataset not found! Place 'yellowtripdata.parquet' in '{parquet_path}'")
        st.stop()


    #  Columns
    df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour
    df["pickup_day"] = df["tpep_pickup_datetime"].dt.dayofweek
    df["pickup_date"] = df["tpep_pickup_datetime"].dt.date
    df["trip_duration_min"] = (
        df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60
    df["tip_pct"] = (df["tip_amount"] / df["fare_amount"] * 100).fillna(0)

    # Clean 
    df = df[(df["fare_amount"] > 0) & (df["fare_amount"] < 200)]
    df = df[(df["trip_distance"] > 0) & (df["trip_distance"] < 50)]
    df = df[(df["trip_duration_min"] > 1) & (df["trip_duration_min"] < 180)]

    return df.reset_index(drop=True)


df = load_data()

# ----------------------- Sidebar -----------------------
st.sidebar.header("Filters")
min_date, max_date = df["pickup_date"].min(), df["pickup_date"].max()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

hour_range = st.sidebar.slider("Hour Range", 0, 23, (0, 23))
payment_map = {1: "Credit Card", 2: "Cash", 3: "No Charge", 4: "Dispute"}

df["payment_name"] = df["payment_type"].map(payment_map)  
df["payment_name"] = df["payment_name"].fillna("Unknown")  

payment_options = st.sidebar.multiselect(
    "Payment Types",
    options=df["payment_name"].unique(),
    default=df["payment_name"].unique()
)

# Filter dataframe by selected payment types
filtered_df = df[df["payment_name"].isin(payment_options)]

# Apply filters
filtered = df[
    (df["pickup_date"] >= date_range[0]) & (df["pickup_date"] <= date_range[1]) &
    (df["pickup_hour"] >= hour_range[0]) & (df["pickup_hour"] <= hour_range[1]) &
    (df["payment_name"].isin(payment_options))
]

# ----------------------- Key Metrics -----------------------
st.subheader("Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Trips", f"{len(filtered):,}")
with col2:
    st.metric("Average Fare", f"${filtered['fare_amount'].mean():.2f}")
with col3:
    st.metric("Total Revenue", f"${filtered['total_amount'].sum():,.2f}")
with col4:
    st.metric("Avg Distance", f"{filtered['trip_distance'].mean():.2f} mi")
with col5:
    st.metric("Avg Duration", f"{filtered['trip_duration_min'].mean():.1f} min")

st.markdown("---")

# ----------------------- Charts -----------------------

# r) Top 10 Pickup Zones
csv_path = "data/raw/zonelookup.csv"
zone_lookup = pd.read_csv(csv_path)
top_zones = filtered.groupby("PULocationID").size().reset_index(name="trips")
top_zones = top_zones.merge(zone_lookup, left_on="PULocationID", right_on="LocationID")
top_zones = top_zones.sort_values("trips", ascending=False).head(10)

fig_r = px.bar(top_zones, x="Zone", y="trips", title="Top 10 Pickup Zones", text="trips")
st.plotly_chart(fig_r, use_container_width=True)
st.markdown("Most trips start in a few very busy areas of the city. This shows that taxi demand is much higher in popular area (see the most comon pair trips previously). Taxi usage is not evenly spread across all zones.")

# s) Average Fare by Hour
avg_fare_hour = (
    filtered.groupby("pickup_hour")["fare_amount"]
    .mean()
    .reset_index()
    .sort_values("pickup_hour")
)
fig_s = px.line(avg_fare_hour, x="pickup_hour", y="fare_amount", markers=True,
                title="Average Fare by Hour")
fig_s.update_yaxes(range=[0, avg_fare_hour["fare_amount"].max()+5], dtick=5)
st.plotly_chart(fig_s, use_container_width=True)
st.markdown("Fares change depending on the time of day. Prices are usually higher during busy hours like morning and evening. This likely happens because more people are traveling at those times.")

# t) Histogram of Trip Distances
fig_t = px.histogram(
    filtered, 
    x="trip_distance", 
    nbins=30,  
    title="Distribution of Trip Distances"
)
fig_t.update_layout(
    xaxis_title="Trip Distance (miles)",
    yaxis_title="Number of Trips",
    bargap=0.05
)
st.plotly_chart(fig_t, use_container_width=True)
st.markdown("Most NYC taxi trips are short, under 5 miles. Longer trips are much less frequent. This shows that local, short-distance rides dominate daily usage.")

# u) Payment Type Breakdown 
payment_counts = (
    filtered.groupby("payment_name")
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)
fig_u = px.bar(payment_counts, x="payment_name", y="count", text="count",
               title="Payment Type Breakdown")
fig_u.update_layout(xaxis_title="Payment Type", yaxis_title="Number of Trips")
st.plotly_chart(fig_u, use_container_width=True)
st.markdown("Most people pay by credit card. Fewer people use cash. This shows that digital payments are more common than cash for taxi rides.")

# v) Heatmap: Trips by Day and Hour
if "pickup_day_of_week" not in filtered.columns:
    filtered["pickup_day_of_week"] = filtered["tpep_pickup_datetime"].dt.dayofweek

bar_data = (
    filtered.groupby(["pickup_day_of_week", "pickup_hour"])
    .size()
    .reset_index(name="trips")
)

weekday_order = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
                 4: "Friday", 5: "Saturday", 6: "Sunday"}
bar_data["pickup_day_name"] = bar_data["pickup_day_of_week"].map(weekday_order)

days_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
bar_pivot = bar_data.pivot(index="pickup_hour", columns="pickup_day_name", values="trips").fillna(0)
bar_pivot = bar_pivot[days_order]  

fig = go.Figure()

for day in days_order:
    fig.add_trace(go.Bar(
        x=bar_pivot.index,   
        y=bar_pivot[day],
        name=day
    ))

fig.update_layout(
    barmode='group',  
    title="Trips by Day of Week and Hour",
    xaxis_title="Hour of Day",
    yaxis_title="Number of Trips",
    xaxis=dict(tickmode='linear', tick0=0, dtick=1)
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("There are more trips during weekday mornings and evenings because of work travel. Weekend nights are also busy due to social activities. Travel patterns clearly change between weekdays and weekends.")