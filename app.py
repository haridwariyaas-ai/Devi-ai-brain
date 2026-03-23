import streamlit as st
from ai_engine.brain import DeviBrain

st.set_page_config(page_title="Devi AI", layout="centered")

st.title("🧠 Devi AI Brain")

st.success("App started successfully ✅")

brain = DeviBrain()

if st.button("Run Devi"):

    try:
        result = brain.run_cycle()
        st.json(result)

    except Exception as e:
        st.error(f"Error: {e}")
