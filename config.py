# config.py

import streamlit as st

def get_secrets():
    try:
        api_key = st.secrets["UPSTOX_API_KEY"]
        access_token = st.secrets["UPSTOX_ACCESS_TOKEN"]
        return api_key, access_token
    except Exception as e:
        return None, None

API_KEY, ACCESS_TOKEN = get_secrets()
