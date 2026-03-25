import streamlit as st
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

st.title("🧠 Devi AI Brain (Clean Version)")

# Fetch price
price = get_nifty_price()

if price == 0:
    st.error("❌ Price fetch failed")
else:
    st.success(f"NIFTY LTP: {price}")

# Fetch OI
oi_data = get_oi_data(price)

if oi_data["call_oi"] == 0 and oi_data["put_oi"] == 0:
    st.error("❌ OI data failed")
else:
    st.write("📊 OI Data")
    st.write(oi_data)
