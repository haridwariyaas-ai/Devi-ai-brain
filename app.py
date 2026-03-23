import streamlit as st
from ai_engine.brain import DeviBrain

st.title("🧠 Devi AI Brain")

brain = DeviBrain()

# ✅ SAFE STARTUP (no auto execution)
st.write("App started successfully ✅")

# ✅ Run only when button clicked
if st.button("Run Devi"):

    try:
        result = brain.run_cycle()
        st.json(result)

    except Exception as e:
        st.error(f"Error: {e}")
