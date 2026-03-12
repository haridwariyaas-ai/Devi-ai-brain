import streamlit as st
import yfinance as yf
from ai_model import train_model

st.title("DEVI AI Brain")

model = train_model()

data = yf.download("^NSEI", period="120d", interval="1d")

data["EMA9"] = data["Close"].ewm(span=9).mean()
data["EMA21"] = data["Close"].ewm(span=21).mean()

data = data.dropna()

latest = data.iloc[-1]

features = [[float(latest["EMA9"]), float(latest["EMA21"]), float(latest["Volume"])]]

prediction = model.predict(features)
prob = model.predict_proba(features)

bull_prob = round(prob[0][1] * 100,2)
bear_prob = round(prob[0][0] * 100,2)

signal = "Bullish" if prediction[0] == 1 else "Bearish"

st.metric("AI Market Prediction", signal)

st.metric("Bullish Probability", str(bull_prob)+"%")
st.metric("Bearish Probability", str(bear_prob)+"%")
