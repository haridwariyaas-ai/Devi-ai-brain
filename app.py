import streamlit as st
from ai_engine.brain import DeviBrain

st.set_page_config(page_title="Devi AI Brain", layout="centered")

st.title("🤖 Devi AI Trading Brain")

# Run AI
brain = DeviBrain()
result = brain.run_cycle()

st.subheader("📊 AI Output")

# Show result properly
st.json(result)
