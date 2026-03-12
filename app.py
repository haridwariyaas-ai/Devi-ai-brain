import streamlit as st

import ai_engine

st.title("DEVI AI Trading Brain")

model,data = ai_engine.train_model()

signal,bull,bear,price = ai_engine.predict_signal(model,data)

st.metric("NIFTY Price", round(price,2))

st.metric("AI Signal", signal)

st.metric("Bullish %", bull)

st.metric("Bearish %", bear)
