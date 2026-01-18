import streamlit as st
import requests
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import time

# Configuration
API_URL = "http://stock_backend:8000"  # Use service name from compose.yaml
st.set_page_config(page_title="Vinod's Stock Portfolio", layout="wide")

st.title("📈 Real-Time Custom Portfolio")

# 1. User Selection (Simulating OPAL Roles)
role = st.sidebar.selectbox("Select Your Role:", ["viewer", "admin"])
st.sidebar.info(f"Current Access Level: {role.upper()}")

# 2. Fetch Authorized Stock List from Backend
def get_authorized_stocks():
    try:
        response = requests.get(f"{API_URL}/stocks", params={"role": role})
        return response.json()
    except Exception as e:
        st.error(f"Could not connect to Backend: {e}")
        return []

# 3. Display Metrics and Charts
placeholder = st.empty()

while True:
    with placeholder.container():
        stocks = get_authorized_stocks()
        
        if not stocks:
            st.warning("No stocks found or you don't have permission to view them.")
        else:
            # Display Top Metrics in Columns
            cols = st.columns(len(stocks))
            for i, s in enumerate(stocks):
                cols[i].metric(label=s['ticker'], value=f"${s['price']}", delta=s['change'])

            # Display Detailed Chart for the first stock
            st.subheader(f"Deep Dive: {stocks[0]['ticker']}")
            hist = yf.download(stocks[0]['ticker'], period="1d", interval="1m")
            
            fig = go.Figure(data=[go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close']
            )])
            fig.update_layout(title=f"{stocks[0]['ticker']} Live 1-Minute Intervals", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

    time.sleep(10)  # Refresh every 10 seconds
