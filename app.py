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
    st.subheader("Nifty 50 Market Overview")
    # This widget is more stable for Nifty 50 on mobile devices
    chart_html = """
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js" async>
      {
        "symbols": [ [ "NSE:NIFTY|1D" ] ],
        "chartOnly": false,
        "width": "100%",
        "height": 500,
        "locale": "in",
        "colorTheme": "dark",
        "autosize": true,
        "showVolume": false,
        "showMA": false,
        "hideDateRanges": false,
        "hideMarketStatus": false,
        "hideSymbolLogo": false,
        "scalePosition": "right",
        "scaleMode": "Normal",
        "fontFamily": "-apple-system, BlinkMacSystemFont, Trebuchet MS, Roboto, Ubuntu, sans-serif",
        "fontSize": "10",
        "noTimeScale": false,
        "valuesTracking": "1",
        "changeMode": "price-and-percent",
        "chartType": "area",
        "maLineColor": "#2962FF",
        "maLineWidth": 1,
        "maLength": 9,
        "lineWidth": 2,
        "lineType": 0,
        "dateRanges": [ "1d", "1m", "3m", "12m", "all" ]
      }
      </script>
    </div>
    """
    st.components.v1.html(chart_html, height=520)

# 3. Live Update Loop
while True:
    try:
        # Get price from WebSocket
        price = get_nifty_price()
        
        # Get OI data
        oi = get_oi_data(price) if price > 0 else {"strike": 0, "call_oi": 0, "put_oi": 0}
        
        with dashboard.container():
            if price == 0:
                st.info("⏳ Connecting to Upstox... (Live data starts at 9:15 AM)")
                st.warning("If this stays at 0, please wait 5 mins without refreshing to clear the 429 Rate Limit.")
            else:
                st.metric("NIFTY 50 LTP", f"₹{price}")
                
                c1, c2, c3 = st.columns(3)
                c1.metric("ATM Strike", oi.get('strike', 0))
                c2.metric("Call OI", f"{oi.get('call_oi', 0):,}")
                c3.metric("Put OI", f"{oi.get('put_oi', 0):,}")
                
                # Signal
                coi, poi = oi.get('call_oi', 0), oi.get('put_oi', 0)
                if poi > coi and poi > 0:
                    st.success("🚀 SIGNAL: BULLISH")
                elif coi > poi and coi > 0:
                    st.warning("🔻 SIGNAL: BEARISH")
                else:
                    st.info("⚖️ SIGNAL: NEUTRAL")

            st.markdown("---")
            st.caption(f"⚡ Last Update: {datetime.now().strftime('%H:%M:%S')}")

    except Exception as e:
        # Silently handle errors to prevent the app from stopping
        pass
    
    # Wait 2 seconds between updates to avoid 429 Rate Limit errors
    time.sleep(2)
