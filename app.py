import streamlit as st
from market_data.upstox_real import get_all_indices

st.set_page_config(page_title="Devi AI Brain", layout="wide")

st.title("🧠 Devi AI Brain")

# --- TOP TICKER ---
# Fetch data once per page load/refresh
with st.spinner("Fetching Market Data..."):
    prices = get_all_indices()

col1, col2, col3 = st.columns(3)

if prices["NIFTY"] > 0:
    col1.metric("NIFTY 50", f"₹{prices['NIFTY']:,}")
    col2.metric("BANK NIFTY", f"₹{prices['BANK_NIFTY']:,}")
    col3.metric("SENSEX", f"₹{prices['SENSEX']:,}")
else:
    st.error("⚠️ Unable to fetch live data. Please check your Access Token.")

st.markdown("---")

# Manual refresh button (Safer for your API limits)
if st.button("🔄 Refresh Prices"):
    st.rerun()

# --- CONTENT TABS ---
tab1, tab2 = st.tabs(["📈 Market Pulse", "🧘 Wellness"])

with tab1:
    st.write("Current Market Status: **Closed** (Showing Friday Close)")
    # Add your trading logic here
