import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os
import subprocess

# ---- Page Configuration ----
st.set_page_config(page_title="FairQuant | Strategy Dashboard", page_icon="📈", layout="wide")
st.markdown("""
    <style>
        .main {background-color: #F5F7FA;}
        h1, h2, h3, h4, .stMetricValue {color: #1E293B; font-family: 'Segoe UI', sans-serif;}
        .stMetricLabel {color: #64748B; font-size: 14px;}
        .block-container {padding-top: 2rem;}
        .metric-container {background-color: white; padding: 1rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 1rem;}
    </style>
""", unsafe_allow_html=True)

# ---- Sidebar Controls ----
st.sidebar.title("🧠 Strategy Controls")
strategy = st.sidebar.selectbox("Select a Strategy", ["sma", "bollinger", "meanrev", "rsi_sma", "momentum"])
short_window = st.sidebar.slider("Short Window", 3, 50, 5)
long_window = st.sidebar.slider("Long Window", 10, 200, 20)
initial_cash = st.sidebar.number_input("Initial Cash", min_value=1000, value=100000)
uploaded_file = st.sidebar.file_uploader("Upload Your CSV Data", type="csv")
data_path = "data/AAPL.csv"

if uploaded_file is not None:
    data_path = "data/uploaded_data.csv"
    with open(data_path, "wb") as f:
        f.write(uploaded_file.read())

# ---- Run Backtest ----
if st.sidebar.button("▶️ Run Backtest"):
    command = (
        f"python main.py "
        f"--strategy {strategy} "
        f"--data {data_path} "
        f"--short {short_window} "
        f"--long {long_window} "
        f"--cash {initial_cash}"
    )
    os.system(command)
    st.success("✅ Backtest executed. Refreshing...")
    st.experimental_rerun()

# ---- Title and Branding ----
st.image("https://i.ibb.co/tKt4bZz/quant-logo.png", width=140)
st.title("FairQuant | Strategy Backtest Dashboard")
st.caption("Explore and compare your trading algorithms with visual insights.")

# ---- Load Data ----
results_path = Path("results/equity_curve.csv")
report_path = Path("results/report.md")
price_chart_path = Path("results/price_signals_plot.png")
equity_chart_path = Path("results/equity_curve_plot.png")

# ---- Tabs ----
tabs = st.tabs(["📈 Charts", "📊 Metrics", "📁 Compare & Export"])

# ---- Charts Tab ----
with tabs[0]:
    st.subheader("Strategy Visualization")
    chart1, chart2 = st.columns(2)

    with chart1:
        if price_chart_path.exists():
            st.image(str(price_chart_path), caption="Price Chart with Trades", use_column_width=True)
        else:
            st.warning("Price chart not found.")

    with chart2:
        if equity_chart_path.exists():
            st.image(str(equity_chart_path), caption="Equity Curve Chart", use_column_width=True)
        else:
            st.warning("Equity chart not found.")

# ---- Metrics Tab ----
with tabs[1]:
    equity_col, metrics_col = st.columns([3, 1])

    with equity_col:
        st.subheader("Equity Curve Over Time")
        if results_path.exists():
            equity_df = pd.read_csv(results_path)
            st.line_chart(equity_df)
        else:
            st.warning("Equity curve not found. Run a backtest first.")

    with metrics_col:
        st.subheader("Summary Metrics")
        if report_path.exists():
            with open(report_path, "r") as f:
                for line in f:
                    if line.startswith("-"):
                        metric = line.replace("- ", "").strip().split(":")
                        if len(metric) == 2:
                            name, value = metric
                            with st.container():
                                st.metric(label=name.strip(), value=value.strip())
        else:
            st.info("Metrics not available yet.")

# ---- Comparison + Export Tab ----
with tabs[2]:
    st.subheader("📁 Compare and Export")
    if results_path.exists():
        st.download_button("📥 Download Equity CSV", data=open(results_path, "rb"), file_name="equity_curve.csv")
    if report_path.exists():
        st.download_button("📥 Download Report (Markdown)", data=open(report_path, "rb"), file_name="backtest_report.md")
    if equity_chart_path.exists():
        st.download_button("📸 Download Equity Curve Image", data=open(equity_chart_path, "rb"), file_name="equity_curve.png")
    if price_chart_path.exists():
        st.download_button("📸 Download Price Chart Image", data=open(price_chart_path, "rb"), file_name="price_chart.png")

# ---- Footer ----
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>Built with ❤️ by <b>FairQuant</b> | Quantitative Strategy Dashboard</p>", unsafe_allow_html=True)
