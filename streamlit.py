import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.loader import load_alerts
from models.prioritizer import rank_alerts

from alert_severity_classifier.src.predict import predict_severity


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Cloud Infrastructure Alert Intelligence",
    page_icon="🚨",
    layout="wide"
)


# ---------------------------------------------------
# Dark Mode Styling
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color:#0E1117;
}

h1,h2,h3 {
    color:#E6EDF3;
}

.stMetric {
    background-color:#161B22;
    padding:15px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title("🚨 Alert prioritization assistant for cloud infrastructure")
st.caption("Real-time prioritization of cloud infrastructure alerts")

st.divider()


# ---------------------------------------------------
# Load Alerts
# ---------------------------------------------------

alerts = load_alerts()

if not alerts:
    st.warning("No alerts found in dataset.")
    st.stop()

ranked_alerts = rank_alerts(alerts)

df = pd.json_normalize(ranked_alerts)


# ---------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------

st.sidebar.header("Dashboard Controls")

refresh_interval = st.sidebar.slider(
    "Auto Refresh (seconds)",
    5,
    60,
    10
)

severity_filter = st.sidebar.multiselect(
    "Filter Severity",
    options=df["severity"].unique(),
    default=df["severity"].unique()
)

status_filter = st.sidebar.multiselect(
    "Filter Status",
    options=df["status"].unique(),
    default=df["status"].unique()
)

df = df[
    (df["severity"].isin(severity_filter)) &
    (df["status"].isin(status_filter))
]


# ---------------------------------------------------
# KPI Metrics
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Alerts", len(df))

col2.metric(
    "Open Alerts",
    (df["status"] == "open").sum()
)

col3.metric(
    "Closed Alerts",
    (df["status"] == "closed").sum()
)

col4.metric(
    "Avg Priority Score",
    round(df["severity"].mean(), 2)
)

st.divider()


# ---------------------------------------------------
# Main Layout
# ---------------------------------------------------

left = st.container()

# ---------------------------------------------------
# Alert Table
# ---------------------------------------------------

with left:

    st.subheader("Alert Inventory")

    table_cols = [
        "id",
        "status",
        "severity",
        "description"
    ]

    st.dataframe(
        df.sort_values("severity", ascending=False)[table_cols],
        use_container_width=True,
    )


# ---------------------------------------------------
# Top Priority Alerts Panel
# ---------------------------------------------------

# with right:

#     st.subheader("🔥 Top Priority Alerts")

#     top_alerts = ranked_alerts[:1]

#     for alert in top_alerts:

#         score = round(alert["severity"], 2)

#         fig = go.Figure(go.Indicator(
#             mode="gauge+number",
#             value=score,
#             title={'text': "Priority Score"},
#             gauge={
#                 'axis': {'range': [0,1]},
#                 'bar': {'color': "#FF4B4B"}
#             }
#         ))

#         st.plotly_chart(fig, use_container_width=True)

#         with st.expander(alert["description"]):

#             st.write("**Status:**", alert["status"])
#             st.write("**Severity:**", alert["severity"])
#             st.write("**Risk:**", alert["risk"])
#             st.write("**Resolution:**", alert["resolution"])

#             st.caption("Feature Signals")
#             st.json(alert["features"])


# st.divider()


# ---------------------------------------------------
# Infrastructure Signal Distributions
# ---------------------------------------------------

st.subheader("Infrastructure Health Signals")

c1, c2 = st.columns(2)

with c1:

    fig_cpu = px.histogram(
        df,
        x="features.CPU_utilization",
        nbins=20,
        title="CPU Utilization Distribution"
    )

    st.plotly_chart(fig_cpu, use_container_width=True)


with c2:

    fig_packet = px.histogram(
        df,
        x="features.packet_loss",
        nbins=20,
        title="Packet Loss Distribution"
    )

    st.plotly_chart(fig_packet, use_container_width=True)


st.divider()


# ---------------------------------------------------
# Severity Heatmap
# ---------------------------------------------------


# ---------------------------------------------------
# Anomaly Detection Visualizations
# ---------------------------------------------------

st.subheader("📊 Performance Anomaly Signals")

c3, c4 = st.columns(2)

with c3:

    fig_scatter = px.scatter(
        df,
        x="features.CPU_utilization",
        y="features.packet_loss",
        color="severity",
        size="severity",
        hover_data=["severity","status"],
        title="CPU vs Packet Loss Anomaly Map"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)


with c4:

    fig_box = px.box(
        df,
        x="severity",
        y="severity",
        color="severity",
        title="Priority Score Distribution by Severity"
    )

    st.plotly_chart(fig_box, use_container_width=True)


st.divider()


# ---------------------------------------------------
# Alert Inspector
# ---------------------------------------------------

st.subheader("🔍 Alert Inspector")

selected_alert = st.selectbox(
    "Select Alert",
    df["description"]
)

alert_data = df[df["description"] == selected_alert]

st.json(alert_data.to_dict(orient="records")[0])


# ---------------------------------------------------
# Auto Refresh
# ---------------------------------------------------

from streamlit_autorefresh import st_autorefresh

st_autorefresh(
    interval=refresh_interval * 1000,
    key="alerts_refresh"
)