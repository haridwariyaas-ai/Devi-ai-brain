import streamlit as st
import time
from market_data.upstox_real import get_all_indices

st.set_page_config(page_title="Devi AI Brain", layout="wide")

# --- TICKER BAR ---
indices = get_all_indices()
t1, t2, t3 = st.columns(3)

# If data is 0, show a loading status
if indices['NIFTY'] == 0:
    st.info("🔄 Connecting to Live Stream... Please wait.")
else:
    t1.metric("NIFTY 50", f"₹{indices['NIFTY']:,}")
    t2.metric("BANK NIFTY", f"₹{indices['BANK_NIFTY']:,}")
    t3.metric("SENSEX", f"₹{indices['SENSEX']:,}")

st.markdown("---")
st.title("🧠 Devi AI Brain Dashboard")
# ... (rest of your app tabs)

# Auto-refresh to see live updates
time.sleep(1)
st.rerun()
