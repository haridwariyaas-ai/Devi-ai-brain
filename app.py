import streamlit as st
from ai_engine.brain import DeviBrain

st.set_page_config(page_title="Devi AI Brain")

st.title("Devi AI Autonomous Trading Brain")

brain = DeviBrain()

if st.button("Run AI Analysis"):

    result = brain.run_cycle()

    st.json(result)
