# app.py

import streamlit as st
from auth.upstox_auth import get_login_url, generate_access_token
from data.upstox_data import get_market_quotes
from scanners.equity_scanner import scan_equity
from logic.reasoning import build_reason

st.set_page_config(page_title="Devi Intraday Scanner", layout="wide")

st.title("🔥 Devi Intraday Scanner")

# =========================
# 🔐 LOGIN SECTION
# =========================

st.subheader("🔐 Upstox Login")

login_url = get_login_url()

st.markdown(f"[👉 Click here to Login]({login_url})")

query_params = st.query_params

# Login ke baad code milega
if "code" in query_params:

    code = query_params["code"]

    if "access_token" not in st.session_state:
        token, error = generate_access_token(code)

        if error:
            st.error(f"Login Failed: {error}")
        else:
            st.session_state["access_token"] = token
            st.success("✅ Login Successful")

# Token check
if "access_token" in st.session_state:
    st.success("✅ Token Active")
else:
    st.warning("⚠️ Please login first")
    st.stop()

# =========================
# 📊 SCANNER SECTION
# =========================

st.subheader("📊 Intraday Scanner")

symbols_input = st.text_input(
    "Enter Stocks",
    "RELIANCE,TCS,HDFCBANK,INFY"
)

if st.button("Run Scanner"):

    try:
        symbols = [s.strip().upper() for s in symbols_input.split(",")]

        df = get_market_quotes(symbols)

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
            st.warning("No strong setups found")

    except Exception as e:
        st.error(f"Error: {str(e)}")
