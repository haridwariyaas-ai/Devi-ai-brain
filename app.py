import streamlit as st

st.set_page_config(page_title="Devi AI Brain", layout="centered")

st.title("🤖 Devi AI Trading Brain")

st.write("🔥 APP LIVE VERSION RUNNING")

from ai_engine.brain import DeviBrain

brain = DeviBrain()

st.write("⚡ Running AI Engine...")

result = brain.run_cycle()

st.subheader("📊 AI Output")
st.json(result)
