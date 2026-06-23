import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PhonePe Payment Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background-color: #f5f3ff; }

    .stApp { background-color: #f5f3ff; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #3d1a78 0%, #5b2d8e 100%);
        color: white;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stSelectbox label { color: #d4b8ff !important; font-size:13px; }

    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 14px;
        padding: 20px 24px;
        box-shadow: 0 2px 12px rgba(93,56,163,0.10);
        border-left: 5px solid #7c3aed;
        margin-bottom: 8px;
    }
    .kpi-value { font-size: 28px; font-weight: 700; color: #3d1a78; margin: 4px 0; }
    .kpi-label { font-size: 13px; color: #888; font-weight: 500; }
    .kpi-delta { font-size: 13px; color: #22c55e; font-weight: 600; }

    /* Section headers */
    .section-title {
        font-size: 18px; font-weight: 700;
        color: #3d1a78; margin: 20px 0 10px 0;
        border-bottom: 2px solid #e9d5ff;
        padding-bottom: 6px;
    }

    /* Insight card */
    .insight-card {
        background: linear-gradient(135deg, #3d1a78, #7c3aed);
        border-radius: 14px;
        padding: 20px;
        color: white;
        margin-top: 10px;
    }
    .insight-card h4 { margin: 0 0 12px 0; font-size: 16px; }
    .insight-card p { font-size: 13px; margin: 6px 0; opacity: 0.92; }

    /* Header banner */
    .header-banner {
        background: linear-gradient(135deg, #3d1a78 0%, #7c3aed 60%, #a855f7 100%);
        border-radius: 16px;
        padding: 24px 32px;
        color: white;
        margin-bottom: 20px;
    }
    .header-banner h1 { margin: 0; font-size: 26px; font-weight: 700; }
    .header-banner p { margin: 6px 0 0; opacity: 0.85; font-size: 14px; }

    div[data-testid="metric-container"] {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(93,56,163,0.08);
        border-left: 4px solid #7c3aed;
    }
</style>
""", unsafe_allow_html=True)

# ── Auto-generate data if not exists ─────────────────────────────────────────
import os
if not os.path.exists("data/phonepe_transactions.csv"):
    os.makedirs("data", exist_ok=True)
    with st.spinner("⏳ Generating dataset for first time... please wait"):
        import subprocess
        subprocess.run(["python", "generate_data.py"], check=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/phonepe_transactions.csv", parse_dates=["date"])
    df["month_num"] = df["date"].dt.month
    df["month"] = df["date"].dt.strftime("%b")
    return df

df = load_data()

MONTH_ORDER = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
PURPLE = "#7c3aed"
LIGHT_PURPLE = "#a855f7"
DARK_PURPLE = "#3d1a78"

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    months = ["All"] + MONTH_ORDER
    sel_month = st.selectbox("📅 Month", months)

    status_opts = ["All", "Successful", "Failed", "Pending"]
    sel_status = st.selectbox("✅ Payment Status", status_opts)

    st.markdown("---")
    st.markdown("### 📌 PhonePe Payment Insights")
    st.markdown("*Secure. Simple. Seamless.*")
    st.markdown("---")
    st.markdown("**Built with:** Python · Streamlit · Plotly")
    st.markdown("**By:** Jayesh Kadam")

# ── Filter Data ───────────────────────────────────────────────────────────────
filtered = df.copy()
if sel_month != "All":
    filtered = filtered[filtered["month"] == sel_month]
if sel_status != "All":
    filtered = filtered[filtered["status"] == sel_status]

success_df = filtered[filtered["status"] == "Successful"]

# ── KPI Calculations ──────────────────────────────────────────────────────────
total_txn = len(filtered)
total_val = success_df["amount"].sum()
total_users = filtered["user_id"].nunique()
success_rate = (filtered["status"] == "Successful").mean() * 100

# MoM growth (approximate)
mom_txn = 8.97
mom_val = 8.98

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <h1>📊 PhonePe Payment Insights Dashboard</h1>
    <p>Analyzing transaction patterns · User behavior · Payment performance</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("💳 Total Transactions", f"{total_txn/1000:.0f}K", f"+{mom_txn}% MoM")
with k2:
    st.metric("💰 Total Value", f"₹{total_val/1e9:.2f}bn", f"+{mom_val}% MoM")
with k3:
    st.metric("👥 Total Users", f"{total_users/1000:.0f}K")
with k4:
    st.metric("✅ Success Rate", f"{success_rate:.2f}%")

st.markdown("---")

# ── Row 1: Transaction Over Time + Age Segment Donut ─────────────────────────
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="section-title">📈 Transaction Over Time</div>', unsafe_allow_html=True)
    monthly = filtered.groupby("month_num").agg(
        count=("transaction_id", "count"),
        value=("amount", "sum"),
        month=("month", "first")
    ).reset_index().sort_values("month_num")

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=monthly["month"], y=monthly["count"],
        name="Total Transaction", mode="lines+markers",
        line=dict(color=PURPLE, width=2.5),
        marker=dict(size=6),
        fill="tozeroy", fillcolor="rgba(124,58,237,0.08)"
    ))
    fig_line.add_trace(go.Scatter(
        x=monthly["month"], y=monthly["value"],
        name="Total Transaction Value", mode="lines+markers",
        line=dict(color="#f59e0b", width=2, dash="dot"),
        marker=dict(size=5), yaxis="y2"
    ))
    fig_line.update_layout(
        height=280, margin=dict(l=10,r=10,t=10,b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        legend=dict(orientation="h", y=-0.25),
        yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
        yaxis2=dict(overlaying="y", side="right", showgrid=False),
        xaxis=dict(categoryorder="array", categoryarray=MONTH_ORDER)
    )
    st.plotly_chart(fig_line, use_container_width=True)

with c2:
    st.markdown('<div class="section-title">👤 Age Segment Contribution</div>', unsafe_allow_html=True)
    age_data = filtered.groupby("age_segment")["amount"].sum().reset_index()
    fig_pie = px.pie(age_data, values="amount", names="age_segment",
                     color_discrete_sequence=["#3d1a78","#7c3aed","#a855f7","#d8b4fe"],
                     hole=0.55)
    fig_pie.update_traces(textposition="outside", textinfo="percent+label")
    fig_pie.update_layout(
        height=280, margin=dict(l=10,r=10,t=10,b=10),
        paper_bgcolor="white", showlegend=True,
        legend=dict(orientation="h", y=-0.15, font=dict(size=11))
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Row 2: Service Analysis + Top Users + Weekday vs Weekend ─────────────────
c3, c4, c5 = st.columns([1.2, 1.2, 1])

with c3:
    st.markdown('<div class="section-title">🏷️ Service Transaction Value</div>', unsafe_allow_html=True)
    svc = success_df.groupby("service_type")["amount"].sum().reset_index().sort_values("amount")
    fig_bar_h = px.bar(svc, x="amount", y="service_type", orientation="h",
                       color_discrete_sequence=[PURPLE])
    fig_bar_h.update_layout(
        height=260, margin=dict(l=10,r=10,t=10,b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#f3f4f6", title=""),
        yaxis=dict(title=""), showlegend=False
    )
    fig_bar_h.update_traces(text=[f"₹{v/1e6:.1f}M" for v in svc["amount"]], textposition="outside")
    st.plotly_chart(fig_bar_h, use_container_width=True)

with c4:
    st.markdown('<div class="section-title">🏆 Top 5 Users (By Value)</div>', unsafe_allow_html=True)
    top5 = success_df.groupby("user_name")["amount"].sum().nlargest(5).reset_index()
    fig_top = px.bar(top5, x="user_name", y="amount",
                     color_discrete_sequence=[LIGHT_PURPLE])
    fig_top.update_layout(
        height=260, margin=dict(l=10,r=10,t=10,b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(title="", tickfont=dict(size=10)),
        yaxis=dict(title="", showgrid=True, gridcolor="#f3f4f6"),
        showlegend=False
    )
    fig_top.update_traces(text=[f"₹{v/1e6:.2f}M" for v in top5["amount"]], textposition="outside")
    st.plotly_chart(fig_top, use_container_width=True)

with c5:
    st.markdown('<div class="section-title">📅 Weekday vs Weekend</div>', unsafe_allow_html=True)
    day_data = filtered.groupby("day_type")["transaction_id"].count().reset_index()
    fig_donut = px.pie(day_data, values="transaction_id", names="day_type",
                       color_discrete_sequence=[PURPLE, "#d8b4fe"],
                       hole=0.55)
    fig_donut.update_traces(textposition="outside", textinfo="percent+label")
    fig_donut.update_layout(
        height=260, margin=dict(l=10,r=10,t=10,b=10),
        paper_bgcolor="white", showlegend=False
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# ── Row 3: Service Type Bar + Insights ───────────────────────────────────────
c6, c7 = st.columns([1.5, 1])

with c6:
    st.markdown('<div class="section-title">📊 Total Transaction by Service Type</div>', unsafe_allow_html=True)
    svc_count = filtered.groupby("service_type")["transaction_id"].count().reset_index()
    fig_svc = px.bar(svc_count, x="service_type", y="transaction_id",
                     color_discrete_sequence=[PURPLE])
    fig_svc.update_layout(
        height=260, margin=dict(l=10,r=10,t=10,b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(title="Service Type"),
        yaxis=dict(title="Total Transaction", showgrid=True, gridcolor="#f3f4f6"),
        showlegend=False
    )
    st.plotly_chart(fig_svc, use_container_width=True)

with c7:
    st.markdown('<div class="section-title">💡 Insights</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="insight-card">
    <h4>📌 Key Insights</h4>
    <p>📈 On Weekdays the number of transactions are maximum.</p>
    <p>💰 Loans service gives the highest transaction value.</p>
    <p>👥 Gen X & Millennials are the top contributors.</p>
    <p>✅ 96% success rate reflects a reliable payment system.</p>
    <p>🏆 Top user generated ₹1.82M+ in transaction value.</p>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center style='color:#888;font-size:13px;'>PhonePe Payment Insights Dashboard · Built with Python & Streamlit · Jayesh Kadam · KBP College of Engineering</center>",
    unsafe_allow_html=True
)
