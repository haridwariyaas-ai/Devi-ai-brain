import streamlit as st
from ai_model import train_model

st.title("DEVI AI Brain")

try:

    model, data = train_model()

    latest = data.iloc[-1]

    ema9 = float(latest["EMA9"])
    ema21 = float(latest["EMA21"])
    volume = float(latest["Volume"])

    features = [[ema9, ema21, volume]]

    prediction = model.predict(features)
    prob = model.predict_proba(features)

    bull_prob = round(prob[0][1]*100,2)
    bear_prob = round(prob[0][0]*100,2)

    signal = "Bullish" if prediction[0] == 1 else "Bearish"

    st.metric("AI Prediction", signal)
    st.metric("Bullish %", bull_prob)
    st.metric("Bearish %", bear_prob)

except Exception as e:

    st.error("Model loading issue")
    st.write(e)
