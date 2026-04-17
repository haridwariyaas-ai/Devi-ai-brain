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
    # This widget is more reliable for restricted indices like Nifty
    chart_html = """
    <iframe src="https://s.tradingview.com/embed-widget/mini-symbol-overview/?symbol=NSE%3ANIFTY&width=100%25&height=400&locale=in&dateRange=1d&colorTheme=dark&trendLineColor=rgba(41, 98, 255, 1)&underLineColor=rgba(41, 98, 255, 0.3)&isTransparent=true&autosize=true" 
    width="100%" height="400" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
    """
    st.components.v1.html(chart_html, height=420)


while True:
    try:
        price = get_nifty_price()
        oi = get_oi_data(price) if price > 0 else {"strike": 0, "call_oi": 0, "put_oi": 0}
        
        with dashboard.container():
            if price == 0:
                st.info("⏳ Connecting to Upstox... (If stuck, wait 5 mins for Rate Limit to reset)")
            else:
                st.metric("NIFTY 50 LTP", f"₹{price}")
                c1, c2, c3 = st.columns(3)
                c1.metric("ATM Strike", oi.get('strike', 0))
                c2.metric("Call OI", f"{oi.get('call_oi', 0):,}")
                c3.metric("Put OI", f"{oi.get('put_oi', 0):,}")
                
                # Signal Logic
                coi, poi = oi.get('call_oi', 0), oi.get('put_oi', 0)
                if poi > coi and poi > 0: st.success("🚀 SIGNAL: BULLISH")
                elif coi > poi and coi > 0: st.warning("🔻 SIGNAL: BEARISH")
                else: st.info("⚖️ SIGNAL: NEUTRAL")

            st.markdown("---")
            st.caption(f"⚡ Last Tick: {datetime.now().strftime('%H:%M:%S')}")

    except Exception:
        pass
    
    time.sleep(2) # Slower loop to prevent 429 errors
