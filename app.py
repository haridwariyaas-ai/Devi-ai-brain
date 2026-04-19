# app.py

import streamlit as st
from data.upstox_data import get_market_quotes
from scanners.equity_scanner import scan_equity
from logic.reasoning import build_reason
from config import ACCESS_TOKEN

st.set_page_config(page_title="Devi Intraday Scanner", layout="wide")

st.title("🔥 Devi Intraday Scanner (REAL DATA)")

# 🔍 DEBUG PANEL
st.subheader("🧪 Debug Info")

if ACCESS_TOKEN:
    st.success("✅ Access Token Loaded")
else:
    st.error("❌ Access Token NOT Loaded (Check Secrets)")

symbols_input = st.text_input(
    "Enter NSE Stocks",
    "RELIANCE,TCS,HDFCBANK,INFY"
)

if st.button("Run Scanner"):

    try:
        symbols = [s.strip().upper() for s in symbols_input.split(",")]

        st.write("📡 Fetching Data...")

        df = get_market_quotes(symbols)

        st.write("📊 Raw Data:")
        st.dataframe(df)

        results = scan_equity(df)

        if results:
            st.success(f"{len(results)} Opportunities Found 🚀")

            for stock in results:
                st.subheader(stock["symbol"])
                st.write(f"Price: ₹{stock['ltp']}")
                st.info(build_reason(stock["signals"]))
                st.markdown("---")
        else:
            st.warning("⚠️ No strong setups found")

    except Exception as e:
        st.error(f"🚨 ERROR: {str(e)}")
