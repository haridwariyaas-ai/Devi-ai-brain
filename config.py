# config.py

import streamlit as st

# Secure credentials from Streamlit Secrets
API_KEY = st.secrets["UPSTOX_API_KEY"]
ACCESS_TOKEN = st.secrets["UPSTOX_ACCESS_TOKEN"]
