# app.py

import streamlit as st
from data.upstox_data import get_market_quotes
from scanners.equity_scanner import scan_equity
from logic.reasoning import build_reason

st.set_page_config(page_title="Devi Intraday Scanner", layout="wide")

st.title("🔥 Devi Intraday Stock Scanner (Real-Time NSE)")

symbols_input = st.text_input(
    "Enter NSE Stocks (comma separated)",
    "RELIANCE,TCS,HDFCBANK,INFY,ICICIBANK"
)

if st.button("Run Scanner"):

    try:
        symbols = [s.strip().upper() for s in symbols_input.split(",")]

        df = get_market_quotes(symbols)

        if df.empty:
            st.warning("No data received from Upstox")
            st.stop()

        results = scan_equity(df)

        if results:
            st.success(f"{len(results)} Opportunities Found 🚀")

            for stock in results:
                st.subheader(stock["symbol"])
                st.write(f"Price: ₹{stock['ltp']}")
                st.info(build_reason(stock["signals"]))
                st.markdown("---")
        else:
            st.warning("No strong intraday setups found")

    except Exception as e:
        st.error(f"Error: {str(e)}")
