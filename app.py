import streamlit as st

st.set_page_config(page_title="Devi AI Brain")

st.title("🤖 Devi AI Trading Brain")

st.write("🔥 Running Live System")

from ai_engine.brain import DeviBrain

brain = DeviBrain()

result = brain.run_cycle()

st.json(result)
