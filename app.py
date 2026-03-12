import streamlit as st
import yfinance as yf
from ai_model import train_model

st.title("DEVI AI Brain")

model = train_model()

data = yf.download("^NSEI", period="120d")

data["EMA9"] = data["Close"].ewm(span=9).mean()
data["EMA21"] = data["Close"].ewm(span=21).mean()

data = data.dropna()

latest = data.iloc[-1]

features = [[latest["EMA9"], latest["EMA21"], latest["Volume"]]]

prediction = model.predict(features)

signal = "Bullish" if prediction[0] == 1 else "Bearish"

st.metric("AI Market Prediction", signal)
