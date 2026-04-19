import streamlit as st

def get_api_details():
    return (
        st.secrets["UPSTOX_API_KEY"],
        st.secrets["UPSTOX_API_SECRET"],
        st.secrets["REDIRECT_URI"]
    )

def get_access_token():
    return st.session_state.get("access_token")

API_KEY, API_SECRET, REDIRECT_URI = get_api_details()
ACCESS_TOKEN = get_access_token()
