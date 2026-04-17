import streamlit as st
import time
from market_data.upstox_real import get_all_indices

st.set_page_config(page_title="Devi AI Brain", layout="wide")

# --- TICKER BAR (Top of App) ---
indices = get_all_indices()
t1, t2, t3 = st.columns(3)

# Displaying the prices with nice formatting
t1.metric("NIFTY 50", f"₹{indices['NIFTY']:,}")
t2.metric("BANK NIFTY", f"₹{indices['BANK_NIFTY']:,}")
t3.metric("SENSEX", f"₹{indices['SENSEX']:,}")

st.markdown("---")

# --- REST OF THE APP ---
st.title("🧠 Devi AI Brain Dashboard")
tab1, tab2 = st.tabs(["📊 Analysis", "🌿 Wellness"])

with tab1:
    st.info("Market is currently CLOSED. Prices above show today's closing values.")
    # Your other trading logic here...

with tab2:
    st.subheader("Trader Mindset")
    # Your Ayurvedic logic here...

# Auto-refresh logic (every 2 seconds)
time.sleep(2)
st.rerun()
