import streamlit as st
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

st.set_page_config(page_title="Devi AI Brain")

st.title("🧠 Devi AI Brain (Stable)")

price = get_nifty_price()

if price == 0:
    st.error("❌ Price fetch failed")
else:
    st.success(f"NIFTY LTP: {price}")

oi_data = get_oi_data(price)

st.write("📊 OI Data:", oi_data)
