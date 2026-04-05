import streamlit as st
import time
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

st.set_page_config(page_title="Devi AI Brain", layout="wide")
st.title("🧠 Devi AI Brain Dashboard")

# Create Tabs
tab1, tab2 = st.tabs(["📊 OI Analysis", "📈 Live Charts"])

with tab1:
    dashboard = st.empty()

with tab2:
    st.subheader("Live Nifty Chart")
    # Using iframe as recommended by your logs to avoid deprecation errors
    chart_url = "https://s.tradingview.com/widgetembed/?frameElementId=tradingview_76292&symbol=NSE%3ANIFTY&interval=1&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme=dark&style=1&timezone=Asia%2FKolkata&studies_overrides={}&overrides={}&enabled_features=[]&disabled_features=[]&locale=in"
    st.components.v1.iframe(chart_url, height=500)

# Live Update Loop for Tab 1
while True:
    price = get_nifty_price()
    oi = get_oi_data(price) if price > 0 else {"strike": 0, "call_oi": 0, "put_oi": 0}
    
    with dashboard.container():
        if price == 0:
            st.info("⏳ Connecting to Upstox WebSocket... (Live only during Market Hours)")
        else:
            st.metric("NIFTY 50 LTP", f"₹{price}")
            c1, c2, c3 = st.columns(3)
            c1.metric("ATM Strike", oi['strike'])
            c2.metric("Call OI", f"{oi['call_oi']:,}")
            c3.metric("Put OI", f"{oi['put_oi']:,}")
            
            # Signal
            if oi['put_oi'] > oi['call_oi'] and oi['put_oi'] > 0:
                st.success("🚀 SIGNAL: BULLISH")
            elif oi['call_oi'] > oi['put_oi'] and oi['call_oi'] > 0:
                st.warning("🔻 SIGNAL: BEARISH")

    time.sleep(0.5) # Tick-by-tick speed
