import requests
import pandas as pd
import streamlit as st
from data.instrument_mapper import get_instrument_key

BASE_URL = "https://api.upstox.com/v2/market-quote/quotes"

def get_market_quotes(symbols):

    token = st.session_state.get("access_token")

    if not token:
        raise Exception("❌ Access Token Missing")

    instrument_keys = []

    for s in symbols:
        key = get_instrument_key(s)
        if key:
            instrument_keys.append(key)

    if not instrument_keys:
        raise Exception("❌ Invalid symbols")

    headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}

    params = {
        "instrument_key": ",".join(instrument_keys)
    }

    res = requests.get(BASE_URL, headers=headers, params=params)

    print("API:", res.text)

    if res.status_code != 200:
        raise Exception(res.text)

    data = res.json().get("data", {})

    if not data:
        raise Exception("❌ No data returned from Upstox")

    rows = []

    for k, v in data.items():
        rows.append({
            "symbol": v.get("tradingsymbol"),
            "ltp": v.get("last_price"),
            "volume": v.get("volume")
        })

    return pd.DataFrame(rows)
