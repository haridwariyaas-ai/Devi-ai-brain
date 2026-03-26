import streamlit as st
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

st.set_page_config(page_title="Devi AI Brain", layout="centered")

st.title("🧠 Devi AI Brain (Final Stable)")

# PRICE
price = get_nifty_price()
st.write("📈 NIFTY LTP:", price)

# OI
oi_data = get_oi_data(price)

st.subheader("📊 OI Data")
st.write(oi_data)
