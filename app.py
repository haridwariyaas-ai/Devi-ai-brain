import streamlit as st
from data_engine.market_data import get_market_data
from ai_brain.model import train_model
from decision_engine.signal import generate_signal
from neural_engine.neural_model import train_neural_model
st.title("DEVI JARVIS Neural AI")

data = get_market_data()

model = train_neural_model(data)

latest = data.iloc[-1]

signal, bull, bear = neural_predict(model, latest)

st.metric("Jarvis Signal", signal)
st.metric("Bullish %", bull)
st.metric("Bearish %", bear)
