import streamlit as st
import time
from datetime import datetime
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

# 1. Page Configuration
st.set_page_config(page_title="Devi AI Brain", layout="wide")

st.title("🧠 Devi AI Brain Dashboard")

# 2. Create Tabs
tab1, tab2 = st.tabs(["📊 OI Analysis", "📈 Live Charts"])

with tab1:
    dashboard = st.empty()

with tab2:
    st.subheader("Nifty 50 Live Chart")
    # Using a specialized TradingView embed that works for Nifty in apps
    chart_url = "https://s.tradingview.com/widgetembed/?symbol=NIFTY&interval=1&theme=dark"
    st.iframe(chart_url, height=500)

# 3. Live Update Loop
while True:
    try:
        price = get_nifty_price()
        oi = get_oi_data(price) if price > 0 else {"strike": 0, "call_oi": 0, "put_oi": 0}
        
        with dashboard.container():
            if price == 0:
                st.info("⏳ Connecting... If this stays at 0, the API is rate-limited (Error 429).")
                st.warning("Please wait 5 minutes without refreshing to reset the connection.")
            else:
                st.metric("NIFTY 50 LTP", f"₹{price}")
                
                c1, c2, c3 = st.columns(3)
                c1.metric("ATM Strike", oi.get('strike', 0))
                c2.metric("Call OI", f"{oi.get('call_oi', 0):,}")
                c3.metric("Put OI", f"{oi.get('put_oi', 0):,}")
                
                # Signal Logic
                coi, poi = oi.get('call_oi', 0), oi.get('put_oi', 0)
                if poi > coi and poi > 0:
                    st.success("🚀 SIGNAL: BULLISH")
                elif coi > poi and coi > 0:
                    st.warning("🔻 SIGNAL: BEARISH")
                else:
                    st.info("⚖️ SIGNAL: NEUTRAL")

            st.markdown("---")
            st.caption(f"⚡ Last Tick: {datetime.now().strftime('%H:%M:%S')}")

    except Exception as e:
        # Prevents the app from crashing completely on errors
        pass
    
    # 1 second delay to prevent 429 Rate Limit errors
    time.sleep(1)
