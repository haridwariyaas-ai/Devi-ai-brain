import streamlit as st
import random

st.title("DEVI AI Brain")

price = random.randint(22000,23000)

st.metric("NIFTY Price", price)

prediction = random.choice(["Bullish","Bearish"])

confidence = random.randint(60,80)

st.metric("AI Prediction", prediction)
st.metric("Confidence", str(confidence)+"%")
