import streamlit as st
import os

st.set_page_config(page_title="Devi AI Brain")

st.title("🤖 Devi AI Trading Brain")

st.write("🔥 Running Live System")

# ✅ ONE-TIME SETUP (AUTO CHECK)
if not os.path.exists("data/instruments.json"):
    st.write("📥 First time setup: Downloading instruments...")

    from market_data.instruments import download_instruments
    download_instruments()

    st.success("✅ Instruments Ready")

# 🔥 NORMAL FLOW
from ai_engine.brain import DeviBrain

brain = DeviBrain()

result = brain.run_cycle()

st.json(result)
