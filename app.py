import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="Devi Zen Trader", layout="wide")

st.title("🌿 Devi Zen: Market & Mindset")

# 2. Ayurvedic Mindset Tracker (Sattvic/Rajasic/Tamasic)
st.sidebar.header("🧘 Ayurvedic Mindset")
mood = st.sidebar.radio(
    "How is your energy right now?",
    ["Sattvic (Calm/Clear)", "Rajasic (High Energy/Aggressive)", "Tamasic (Dull/Confused)"]
)

if "Sattvic" in mood:
    st.sidebar.success("✅ Good time for deep analysis.")
elif "Rajasic" in mood:
    st.sidebar.warning("⚡ High energy. Avoid impulsive trades.")
else:
    st.sidebar.error("💤 Low focus. Better to stay away from the screen.")

# 3. Create Tabs
tab1, tab2 = st.tabs(["📊 Market Pulse", "📈 Analysis Chart"])

with tab1:
    st.subheader("Global Market Sentiment")
    # This widget shows the 'Technical Rating' for Nifty 50 instantly
    gauge_html = """
    <div style="height:400px;">
    <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol=NSE%3ANIFTY&interval=1m&theme=dark&locale=in" 
    width="100%" height="400" frameborder="0" allowtransparency="true"></iframe>
    </div>
    """
    st.components.v1.html(gauge_html, height=450)

with tab2:
    st.subheader("Live Price Action")
    # Reliable mobile-friendly chart
    chart_url = "https://s.tradingview.com/widgetembed/?symbol=NSE%3ANIFTY&interval=5&theme=dark"
    st.iframe(chart_url, height=500)

# 4. Simple Trading Journal
st.markdown("---")
st.subheader("📝 Quick Trade Log")
col1, col2 = st.columns(2)
with col1:
    entry = st.number_input("Entry Price", value=22000)
    side = st.selectbox("Side", ["BUY", "SELL"])
with col2:
    target = st.number_input("Target", value=22100)
    stop = st.number_input("Stop Loss", value=21950)

if st.button("Calculate Risk/Reward"):
    rr = abs(target - entry) / abs(entry - stop)
    st.info(f"Your Risk/Reward Ratio is 1 : {rr:.2f}")

st.caption(f"Last Refresh: {datetime.now().strftime('%H:%M:%S')}")
