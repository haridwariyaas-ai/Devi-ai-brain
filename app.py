
import streamlit as st
from ai_engine.brain import DeviBrain

st.set_page_config(page_title="Devi AI Brain V2")

st.title("Devi AI Autonomous Trading Brain")

brain = DeviBrain()

if st.button("Run AI Cycle"):
    result = brain.run_cycle()
    st.json(result)
