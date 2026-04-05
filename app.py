import streamlit as st
import time
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

st.set_page_config(page_title="Devi AI Brain", layout="wide")

st.title("🧠 Devi AI Brain Dashboard")

# 1. Create Tabs
tab1, tab2 = st.tabs(["📊 OI Analysis", "📈 Live Charts"])

with tab1:
    # --- Your existing OI Logic ---
    live_container = st.empty()

with tab2:
    st.subheader("Live Nifty Chart (TradingView)")
    # Since Upstox doesn't have an embed, we use the standard TradingView Widget
    # which shows the same Nifty data and is very fast.
    chart_html = """
    <div class="tradingview-widget-container" style="height:500px;">
      <div id="tradingview_12345" style="height:500px;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true,
        "symbol": "NSE:NIFTY",
        "interval": "1",
        "timezone": "Asia/Kolkata",
        "theme": "dark",
        "style": "1",
        "locale": "in",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_top_toolbar": false,
        "save_image": false,
        "container_id": "tradingview_12345"
      });
      </script>
    </div>
    """
    st.components.v1.html(chart_html, height=520)

# --- Update Loop for Tab 1 ---
while True:
    price = get_nifty_price()
    oi = get_oi_data(price)
    
    with live_container.container():
        st.metric("Nifty LTP", price)
        c1, c2 = st.columns(2)
        c1.metric("Call OI", f"{oi['call_oi']:,}")
        c2.metric("Put OI", f"{oi['put_oi']:,}")
    
    time.sleep(1)
