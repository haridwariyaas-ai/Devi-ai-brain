import streamlit as st
from ai_engine import train_model,predict_signal

st.title("DEVI AI Trading Brain")

model,data = train_model()

signal,bull,bear,price = predict_signal(model,data)

st.metric("NIFTY Price",round(price,2))
st.metric("AI Signal",signal)
st.metric("Bullish %",bull)
st.metric("Bearish %",bear)
