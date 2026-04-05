import streamlit as st
import time
from datetime import datetime
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

# 1. Page Configuration
st.set_page_config(page_title="Devi AI Brain", layout="centered")

st.title("🧠 Devi AI Brain")

# 2. Create a placeholder for live updates
# This prevents the app from creating a long list of updates
live_dashboard = st.empty()

# 3. Live Update Loop
while True:
    with live_dashboard.container():
        # =========================
        # PRICE FETCHING
        # =========================
        price = get_nifty_price()

        if price == 0:
            st.error("❌ Price fetch failed. Retrying...")
        else:
            st.success(f"📈 NIFTY LTP: {price}")

            # =========================
            # OI ANALYSIS
            # =========================
            # Ensure get_oi_data in upstox_oi.py returns call_oi and put_oi
            oi = get_oi_data(price)

            st.subheader("📊 Live OI Analysis")
            
            # Using columns for a cleaner "Tick-by-Tick" look
            col1, col2, col3 = st.columns(3)
            col1.metric("ATM Strike", oi.get('strike', 0))
            col2.metric("Call OI", f"{oi.get('call_oi', 0):,}")
            col3.metric("Put OI", f"{oi.get('put_oi', 0):,}")

            # =========================
            # SIGNAL LOGIC
            # =========================
            call_oi = oi.get('call_oi', 0)
            put_oi = oi.get('put_oi', 0)

            if put_oi > call_oi and put_oi > 0:
                st.success("🚀 SIGNAL: Bullish (Put OI > Call OI)")
            elif call_oi > put_oi and call_oi > 0:
                st.warning("🔻 SIGNAL: Bearish (Call OI > Put OI)")
            else:
                st.info("⚖️ SIGNAL: Neutral / Waiting for Data")
            
            # Weekend/Holiday Check (April 5, 2026 is a Sunday)
            if datetime.now().strftime("%A") in ["Saturday", "Sunday"]:
                st.warning("⚠️ Market is Closed. Showing last available or zero data.")

        # =========================
        # FOOTER
        # =========================
        st.markdown("---")
        st.caption(f"⚡ Last Tick: {datetime.now().strftime('%H:%M:%S')} | Powered by Devi AI Brain")

    # 4. Refresh rate (1 second for tick-by-tick)
    time.sleep(1)
