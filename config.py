# config.py

import streamlit as st

def get_access_token():
    # Session se token lo (login ke baad)
    if "access_token" in st.session_state:
        return st.session_state["access_token"]
    return None

def get_api_details():
    try:
        api_key = st.secrets["UPSTOX_API_KEY"]
        api_secret = st.secrets["UPSTOX_API_SECRET"]
        redirect_uri = st.secrets["REDIRECT_URI"]
        return api_key, api_secret, redirect_uri
    except:
        return None, None, None

ACCESS_TOKEN = get_access_token()
API_KEY, API_SECRET, REDIRECT_URI = get_api_details()
