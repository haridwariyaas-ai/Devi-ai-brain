import streamlit as st
import time
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

st.set_page_config(page_title="Devi AI Brain", layout="wide")
st.title("🧠 Devi AI Brain: Live WebSocket Feed")

# Placeholder for the live dashboard
dashboard = st.empty()

while True:
    # 1. Fetch current price from the WebSocket variable
    price = get_nifty_price()
    
    # 2. Fetch OI (this uses the REST API)
    oi = get_oi_data(price) if price > 0 else {"strike": 0, "call_oi": 0, "put_oi": 0}

    with dashboard.container():
        # Display Price
        if price == 0:
            st.info("⏳ Waiting for WebSocket connection... (Market must be OPEN)")
        else:
            st.metric("NIFTY 50 LTP", f"₹{price}", delta_color="normal")
            
            # Display OI
            col1, col2, col3 = st.columns(3)
            col1.metric("ATM Strike", oi['strike'])
            col2.metric("Call OI", f"{oi['call_oi']:,}")
            col3.metric("Put OI", f"{oi['put_oi']:,}")

    # Sleep for high-frequency "Tick-by-Tick" updates
    time.sleep(0.5)
