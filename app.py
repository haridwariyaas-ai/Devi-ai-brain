import streamlit as st
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

st.title("🧠 Devi AI Brain (Option Chain Mode)")

price = get_nifty_price()
st.write("📈 NIFTY LTP:", price)

oi = get_oi_data(price)
st.write("📊 OI DATA:", oi)
