import streamlit as st
from data_engine.market_data import get_market_data
from ai_brain.model import train_model
from decision_engine.signal import generate_signal

st.title("DEVI JARVIS AI")

data = get_market_data()

model = train_model(data)

latest = data.iloc[-1]

signal, bull, bear = generate_signal(model, latest)

st.metric("AI Signal", signal)
st.metric("Bullish %", bull)
st.metric("Bearish %", bear)
