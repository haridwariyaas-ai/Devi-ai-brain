import streamlit as st
from ai_engine.brain import DeviBrain

st.title("🧠 Devi AI Brain")

brain = DeviBrain()

if st.button("Run Devi"):

    result = brain.run_cycle()

    st.json(result)
