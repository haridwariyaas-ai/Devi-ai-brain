import streamlit as st
import time
from datetime import datetime
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

st.set_page_config(page_title="Devi AI Brain", layout="wide")
st.title("🧠 Devi AI Brain Dashboard")

tab1, tab2 = st.tabs(["📊 OI Analysis", "📈 Live Charts"])

with tab1:
    dashboard = st.empty()

with tab2:
    st.subheader("Nifty 50 Trend")
    # Using the 'Mini Chart' which is highly reliable for indexes
    chart_html = """
    <iframe src="https://s.tradingview.com/embed-widget/mini-symbol-overview/?symbol=NSE%3ANIFTY&width=100%25&height=400&locale=in&dateRange=1d&colorTheme=dark&isTransparent=true&autosize=true" 
    width="100%" height="400" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
    """
    st.components.v1.html(chart_html, height=420)

while True:
    try:
        price = get_nifty_price()
        oi = get_oi_data(price) if price > 0 else {"strike": 0, "call_oi": 0, "put_oi": 0}
        
        with dashboard.container():
            if price == 0:
                st.info("⏳ Establishing secure connection to Upstox...")
                st.warning("If this takes more than 1 minute, please do not refresh. The system is clearing a 429 Rate Limit.")
            else:
                st.metric("NIFTY 50 LTP", f"₹{price}")
                c1, c2, c3 = st.columns(3)
                c1.metric("ATM Strike", oi.get('strike', 0))
                c2.metric("Call OI", f"{oi.get('call_oi', 0):,}")
                c3.metric("Put OI", f"{oi.get('put_oi', 0):,}")

            st.markdown("---")
            st.caption(f"⚡ Last Heartbeat: {datetime.now().strftime('%H:%M:%S')}")
    except:
        pass
    
    time.sleep(2) # Prevent high-frequency API calls
