import streamlit as st
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

st.set_page_config(page_title="Devi AI Brain", layout="centered")

st.title("🧠 Devi AI Brain (Stable Version)")

# Fetch price
price = get_nifty_price()

if price == 0:
    st.error("❌ Price fetch failed (Check Token)")
    st.stop()

st.success(f"📈 NIFTY LTP: {price}")

# Fetch OI
oi_data = get_oi_data(price)

st.subheader("📊 OI Data")

if oi_data["call_oi"] == 0 and oi_data["put_oi"] == 0:
    st.warning("⚠️ OI not available / Market closed")
else:
    st.write(oi_data)
