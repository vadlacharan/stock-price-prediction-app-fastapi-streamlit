import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Price Prediction")
# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"

STOCK_TICKERS = ["RELIANCE","ONGC","SBIN","ADANIGREEN","ICICIPRULI"]

st.title("Stock Price Prediction App")

st.sidebar.header("Input Parameters")

ticker = st.sidebar.selectbox("Select Stock Ticker:", STOCK_TICKERS)

default_date = datetime.now()
start_date = st.sidebar.date_input(
    "Select Start Date:", 
    min_value=datetime(2000, 1, 1), 
    max_value=default_date, 
    value=default_date - timedelta(days=7)
)

days = st.sidebar.number_input(
    "Number of Days to Predict:", 
    min_value=1, 
    max_value=30, 
    value=7, 
    step=1
)

if st.sidebar.button("Predict"):
    with st.spinner("Fetching predictions..."):
        formatted_start_date = start_date.strftime("%Y-%m-%d")
        
        response = requests.get(
            f"{BACKEND_URL}/predict",
            params={"ticker": ticker, "days": days, "start_date": formatted_start_date}
        )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                forecast = pd.DataFrame(data["forecast"])

                st.subheader(f"Stock Price Prediction for {ticker.upper()} (Next {days} Days)")
                st.write(f"Start Date: {formatted_start_date}")
                st.dataframe(forecast)

                fig = px.line(
                    forecast,
                    x="ds",
                    y="yhat",
                    title=f"Predicted Prices for {ticker.upper()}",
                    labels={"ds": "Date", "yhat": "Predicted Price"},
                )
                fig.add_scatter(x=forecast["ds"], y=forecast["yhat_lower"], mode="lines", name="Lower Bound")
                fig.add_scatter(x=forecast["ds"], y=forecast["yhat_upper"], mode="lines", name="Upper Bound")
                st.plotly_chart(fig)
            else:
                st.error(data["error"])
        else:
            st.error("Failed to fetch data. Please check the backend.")
