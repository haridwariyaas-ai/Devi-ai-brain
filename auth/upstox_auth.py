# auth/upstox_auth.py

import requests
import streamlit as st

API_KEY = st.secrets["UPSTOX_API_KEY"]
API_SECRET = st.secrets["UPSTOX_API_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]

def get_login_url():
    return f"https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={API_KEY}&redirect_uri={REDIRECT_URI}"


def generate_access_token(code):

    url = "https://api.upstox.com/v2/login/authorization/token"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "code": code,
        "client_id": API_KEY,
        "client_secret": API_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        st.error(response.text)
        return None

    return response.json().get("access_token")
