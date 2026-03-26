import streamlit as st
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

st.set_page_config(page_title="Devi AI Brain", layout="centered")

st.title("🧠 Devi AI Brain")

# =========================
# PRICE
# =========================
price = get_nifty_price()

if price == 0:
    st.error("❌ Price fetch failed")
    st.stop()

st.success(f"📈 NIFTY LTP: {price}")

# =========================
# OI
# =========================
oi = get_oi_data(price)

st.subheader("📊 OI Analysis")

st.write(f"🎯 ATM Strike: {oi['strike']}")
st.write(f"📈 Call OI: {oi['call_oi']}")
st.write(f"📉 Put OI: {oi['put_oi']}")

# =========================
# SIGNAL
# =========================
if oi["put_oi"] > oi["call_oi"]:
    st.success("📈 Bullish (Put OI > Call OI)")
elif oi["call_oi"] > oi["put_oi"]:
    st.warning("📉 Bearish (Call OI > Put OI)")
else:
    st.info("⚖️ Neutral")

st.markdown("---")
st.caption("⚡ Powered by Devi AI Brain")
