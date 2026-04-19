# data/upstox_data.py

import requests
import pandas as pd
from config import ACCESS_TOKEN

BASE_URL = "https://api.upstox.com/v2/market-quote/quotes"

def get_market_quotes(symbols):

    if not ACCESS_TOKEN:
        raise Exception("❌ Access Token Missing from Streamlit Secrets")

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    instrument_keys = [f"NSE_EQ|{symbol}" for symbol in symbols]

    params = {
        "instrument_key": ",".join(instrument_keys)
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    # 🔍 DEBUG OUTPUT (IMPORTANT)
    print("STATUS CODE:", response.status_code)
    print("RAW RESPONSE:", response.text)

    if response.status_code != 200:
        raise Exception(f"❌ API Error: {response.text}")

    json_data = response.json()

    if "data" not in json_data or not json_data["data"]:
        raise Exception("❌ No data returned from Upstox (Token expired or wrong symbols)")

    rows = []

    for key, val in json_data["data"].items():
        rows.append({
            "symbol": key.split("|")[1],
            "ltp": val.get("last_price"),
            "volume": val.get("volume")
        })

    df = pd.DataFrame(rows)

    if df.empty:
        raise Exception("❌ DataFrame empty after processing")

    return df
