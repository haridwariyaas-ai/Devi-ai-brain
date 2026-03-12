import streamlit as st
import yfinance as yf

st.title("DEVI AI Brain")

# NIFTY data
data = yf.Ticker("^NSEI")

df = data.history(period="1d")

price = df["Close"].iloc[-1]

st.metric("NIFTY Price", round(price,2))

# simple AI logic
if df["Close"].iloc[-1] > df["Open"].iloc[-1]:
    prediction = "Bullish"
else:
    prediction = "Bearish"

st.metric("AI Prediction", prediction)
