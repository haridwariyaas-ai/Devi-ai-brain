# data/upstox_data.py

import requests
import pandas as pd
import streamlit as st

BASE_URL = "https://api.upstox.com/v2/market-quote/quotes"

def get_market_quotes(symbols):

    # 🔥 SESSION se token lo (IMPORTANT FIX)
    access_token = st.session_state.get("access_token")

    if not access_token:
        raise Exception("❌ Access Token Missing (Login again)")

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    instrument_keys = [f"NSE_EQ|{s}" for s in symbols]

    params = {
        "instrument_key": ",".join(instrument_keys)
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    if response.status_code == 401:
        raise Exception("❌ Token Expired")

    if response.status_code != 200:
        raise Exception(f"❌ API Error: {response.text}")

    data = response.json()

    if "data" not in data or not data["data"]:
        raise Exception("❌ No data returned from Upstox")

    rows = []

    for key, val in data["data"].items():
        rows.append({
            "symbol": key.split("|")[1],
            "ltp": val.get("last_price"),
            "volume": val.get("volume")
        })

    df = pd.DataFrame(rows)

    return df
