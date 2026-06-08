import streamlit as st
from google.cloud import bigquery
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="NYC 311 Analytics",
    page_icon="🗽",
    layout="wide"
)

# BigQuery client
@st.cache_resource
def get_client():
    import google.oauth2.credentials
    secrets = st.secrets["gcp_service_account"]
    credentials = google.oauth2.credentials.Credentials(
        token=None,
        refresh_token=secrets["refresh_token"],
        client_id=secrets["client_id"],
        client_secret=secrets["client_secret"],
        token_uri="https://oauth2.googleapis.com/token"
    )
    return bigquery.Client(project="nyc311-analytics", credentials=credentials)

@st.cache_data(ttl=3600)
def run_query(query):
    client = get_client()
    return client.query(query).to_dataframe()

# Load data
@st.cache_data(ttl=3600)
def load_agency_data():
    return run_query("SELECT * FROM `nyc311-analytics.nyc311_dev.mart_agency_performance`")

@st.cache_data(ttl=3600)
def load_borough_data():
    return run_query("SELECT * FROM `nyc311-analytics.nyc311_dev.mart_borough_complaints`")

@st.cache_data(ttl=3600)
def load_trends_data():
    return run_query("SELECT * FROM `nyc311-analytics.nyc311_dev.mart_monthly_trends`")

# Sidebar navigation
st.sidebar.title("🗽 NYC 311 Analytics")
page = st.sidebar.radio("Navigate", [
    "Executive Summary",
    "Agency Performance",
    "Borough Analysis",
    "Trend Analysis"
])

# ── PAGE 1: Executive Summary ──────────────────────────────────────────
if page == "Executive Summary":
    st.title("🗽 NYC 311 Service Request Analytics")
    st.markdown("**End-to-end analytics engineering project · dbt Core + BigQuery + Streamlit**")

    agency_df = load_agency_data()

    total_requests = agency_df["total_requests"].sum()
    avg_response   = round(agency_df["avg_response_hours"].mean(), 1)
    avg_sla        = round(agency_df["sla_compliance_pct"].mean(), 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Requests", f"{total_requests:,}")
    col2.metric("Avg Response Time", f"{avg_response} hrs")
    col3.metric("Avg SLA Compliance", f"{avg_sla}%")

    st.divider()
    st.subheader("Top 10 Agencies by Request Volume")
    top10 = agency_df.nlargest(10, "total_requests")
    fig = px.bar(top10, x="total_requests", y="agency_name",
                 orientation="h", color="sla_compliance_pct",
                 color_continuous_scale="RdYlGn",
                 labels={"total_requests": "Total Requests",
                         "agency_name": "Agency",
                         "sla_compliance_pct": "SLA %"})
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

# ── PAGE 2: Agency Performance ─────────────────────────────────────────
elif page == "Agency Performance":
    st.title("🏛️ Agency Performance Scorecard")

    agency_df = load_agency_data()

    st.subheader("SLA Compliance by Agency")
    fig = px.scatter(agency_df, x="avg_response_hours", y="sla_compliance_pct",
                     size="total_requests", hover_name="agency_name",
                     color="sla_compliance_pct", color_continuous_scale="RdYlGn",
                     labels={"avg_response_hours": "Avg Response Hours",
                             "sla_compliance_pct": "SLA Compliance %"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Bottom 10 Agencies by SLA Compliance")
    worst = agency_df.nsmallest(10, "sla_compliance_pct")[
        ["agency_name", "total_requests", "avg_response_hours", "sla_compliance_pct"]
    ].reset_index(drop=True)
    st.dataframe(worst, use_container_width=True)

# ── PAGE 3: Borough Analysis ───────────────────────────────────────────
elif page == "Borough Analysis":
    st.title("🗺️ Borough Complaint Analysis")

    borough_df = load_borough_data()

    borough_totals = borough_df.groupby("borough")["total_requests"].sum().reset_index()
    fig = px.bar(borough_totals, x="borough", y="total_requests",
                 color="total_requests", color_continuous_scale="Blues",
                 labels={"total_requests": "Total Requests", "borough": "Borough"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Complaint Types by Borough")
    selected_borough = st.selectbox("Select Borough", borough_df["borough"].unique())
    filtered = borough_df[borough_df["borough"] == selected_borough].nlargest(10, "total_requests")
    fig2 = px.bar(filtered, x="total_requests", y="complaint_type", orientation="h",
                  labels={"total_requests": "Total Requests", "complaint_type": "Complaint Type"})
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig2, use_container_width=True)

# ── PAGE 4: Trend Analysis ─────────────────────────────────────────────
elif page == "Trend Analysis":
    st.title("📈 Trend Analysis")

    trends_df = load_trends_data()

    st.subheader("Monthly Request Volume by Complaint Type")
    top_complaints = trends_df.groupby("complaint_type")["total_requests"].sum().nlargest(5).index.tolist()
    selected = st.multiselect("Select Complaint Types", top_complaints, default=top_complaints[:3])

    filtered = trends_df[trends_df["complaint_type"].isin(selected)]
    monthly = filtered.groupby(["year_month", "complaint_type"])["total_requests"].sum().reset_index()
    fig = px.line(monthly, x="year_month", y="total_requests", color="complaint_type",
                  labels={"year_month": "Month", "total_requests": "Requests", "complaint_type": "Type"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Request Volume Heatmap: Day of Week × Hour")
    trends_df2 = run_query("""
        SELECT day_of_week, request_hour, COUNT(*) as total_requests
        FROM `nyc311-analytics.nyc311_dev.int_requests_enriched`
        GROUP BY day_of_week, request_hour
    """)
    pivot = trends_df2.pivot(index="day_of_week", columns="request_hour", values="total_requests")
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    pivot = pivot.reindex([d for d in day_order if d in pivot.index])
    fig2 = px.imshow(pivot, color_continuous_scale="Blues",
                     labels={"x": "Hour of Day", "y": "Day of Week", "color": "Requests"})
    st.plotly_chart(fig2, use_container_width=True)