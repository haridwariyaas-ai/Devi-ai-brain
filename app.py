import streamlit as st
import yfinance as yf
from ai_model import train_model

st.title("DEVI AI Brain")

model = train_model()

data = yf.download("^NSEI", period="5d", interval="1d")

latest = data.iloc[-1]

features = [[latest["Close"], latest["Close"], latest["Volume"]]]

prediction = model.predict(features)

if prediction == 1:
    signal = "Bullish"
else:
    signal = "Bearish"

st.metric("AI Market Prediction", signal)
