import streamlit as st
import time
from datetime import datetime
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

# 1. Page Configuration
st.set_page_config(page_title="Devi AI Brain", layout="wide")

st.title("🧠 Devi AI Brain Dashboard")

# 2. Create Tabs for Navigation
tab1, tab2 = st.tabs(["📊 OI Analysis", "📈 Live Charts"])

with tab1:
    # This placeholder allows us to refresh data without flickering
    dashboard = st.empty()

with tab2:
    st.subheader("Nifty 50 Live Chart")
    # Using a direct, mobile-friendly TradingView embed
    # We use st.iframe as recommended by Streamlit logs for better compatibility
    chart_url = "https://s.tradingview.com/widgetembed/?symbol=NSE%3ANIFTY&interval=1&theme=dark"
    st.iframe(chart_url, height=500, scrolling=True)

# 3. Live Update Loop
# This loop runs continuously to provide tick-by-tick updates
while True:
    # Fetch live price from the WebSocket in upstox_real.py
    price = get_nifty_price()
    
    # Fetch OI data from the API in upstox_oi.py
    # We only call this if price is valid (> 0)
    oi = get_oi_data(price) if price > 0 else {"strike": 0, "call_oi": 0, "put_oi": 0}
    
    with dashboard.container():
        if price == 0:
            st.info("⏳ Connecting to Upstox WebSocket... (Live data starts Monday 9:15 AM)")
            if datetime.now().strftime("%A") in ["Saturday", "Sunday"]:
                st.warning("Note: Markets are currently closed. WebSocket will not push live ticks today.")
        else:
            # Display Price Metric
            st.metric("NIFTY 50 LTP", f"₹{price}")
            
            # Display OI Metrics in 3 columns
            c1, c2, c3 = st.columns(3)
            c1.metric("ATM Strike", oi.get('strike', 0))
            c2.metric("Call OI", f"{oi.get('call_oi', 0):,}")
            c3.metric("Put OI", f"{oi.get('put_oi', 0):,}")
            
            # Signal Logic
            call_oi = oi.get('call_oi', 0)
            put_oi = oi.get('put_oi', 0)
            
            if put_oi > call_oi and put_oi > 0:
                st.success("🚀 SIGNAL: BULLISH (Put OI > Call OI)")
            elif call_oi > put_oi and call_oi > 0:
                st.warning("🔻 SIGNAL: BEARISH (Call OI > Put OI)")
            else:
                st.info("⚖️ SIGNAL: NEUTRAL")

        # Footer with timestamp
        st.markdown("---")
        st.caption(f"⚡ Last Update: {datetime.now().strftime('%H:%M:%S')} | Device: Mobile Optimized")

    # Refresh frequency (0.5 seconds for high-speed tracking)
    time.sleep(0.5)
