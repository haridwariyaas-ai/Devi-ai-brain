import streamlit as st
from market_data.upstox_real import get_nifty_price
from market_data.upstox_oi import get_oi_data

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Devi AI Brain",
    layout="centered"
)

st.title("🧠 Devi AI Brain")

# =========================
# FETCH PRICE
# =========================
price = get_nifty_price()

if price == 0:
    st.error("❌ Price fetch failed (Check token/API)")
    st.stop()

st.success(f"📈 NIFTY LTP: {price}")

# =========================
# FETCH OI DATA
# =========================
oi_data = get_oi_data(price)

# =========================
# DISPLAY OI
# =========================
st.subheader("📊 OI Analysis")

strike = oi_data.get("strike", 0)
call_oi = oi_data.get("call_oi", 0)
put_oi = oi_data.get("put_oi", 0)

st.write(f"🎯 Strike (ATM): {strike}")
st.write(f"📈 Call OI: {call_oi}")
st.write(f"📉 Put OI: {put_oi}")

# =========================
# BASIC INSIGHT
# =========================
if call_oi > put_oi:
    st.warning("📉 Bearish Pressure (Call OI > Put OI)")
elif put_oi > call_oi:
    st.success("📈 Bullish Pressure (Put OI > Call OI)")
else:
    st.info("⚖️ Neutral Market")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("⚡ Powered by Devi AI Brain")
