import streamlit as st
from auth.upstox_auth import get_login_url, generate_access_token
from data.upstox_data import get_market_quotes

st.title("🔥 Devi Scanner")

# LOGIN
login_url = get_login_url()
st.markdown(f"[Login to Upstox]({login_url})")

params = st.query_params

if "code" in params and "access_token" not in st.session_state:

    code = params["code"][0] if isinstance(params["code"], list) else params["code"]

    token, err = generate_access_token(code)

    if err:
        st.error(err)
    else:
        st.session_state["access_token"] = token
        st.success("Login Success")
        st.rerun()

if "access_token" not in st.session_state:
    st.warning("Login first")
    st.stop()

st.success("Token Active")

# SCANNER
symbols = st.text_input("Enter Stocks", "RELIANCE")

if st.button("Run Scanner"):

    try:
        sym_list = [s.strip().upper() for s in symbols.split(",")]

        df = get_market_quotes(sym_list)

        st.dataframe(df)

    except Exception as e:
        st.error(str(e))
