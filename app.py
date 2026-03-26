import streamlit as st
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

st.title("🧠 Devi AI Brain")

# 🔥 FORCE PRICE
price = get_nifty_price()
st.write("📈 Price:", price)

# 🔥 FORCE OI CALL (NO STOP)
oi_data = get_oi_data(price)

st.write("📊 OI RESULT:", oi_data)
