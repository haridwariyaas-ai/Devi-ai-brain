import streamlit as st

st.set_page_config(page_title="Devi AI Brain", layout="centered")

st.title("🤖 Devi AI Trading Brain")

# DEBUG (force check)
st.write("🔥 APP NEW VERSION RUNNING")

from ai_engine.brain import DeviBrain

brain = DeviBrain()

st.write("⚡ Running AI Engine...")

result = brain.run_cycle()

st.subheader("📊 AI Output")
st.json(result)
