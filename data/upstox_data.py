# data/upstox_data.py

import requests
import pandas as pd
from config import ACCESS_TOKEN

BASE_URL = "https://api.upstox.com/v2/market-quote/quotes"

def get_market_quotes(symbols):

    if not ACCESS_TOKEN:
        raise Exception("❌ Access Token Missing")

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    instrument_keys = [f"NSE_EQ|{s}" for s in symbols]

    params = {
        "instrument_key": ",".join(instrument_keys)
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    # 🔍 DEBUG (VERY IMPORTANT)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    # ❌ TOKEN INVALID
    if response.status_code == 401:
        raise Exception("❌ Token Expired / Unauthorized")

    # ❌ OTHER ERROR
    if response.status_code != 200:
        raise Exception(f"❌ API Error: {response.text}")

    data = response.json()

    # ❌ EMPTY RESPONSE
    if "data" not in data or not data["data"]:
        raise Exception("❌ No data from Upstox (Token expired OR wrong symbol)")

    rows = []

    for key, val in data["data"].items():
        rows.append({
            "symbol": key.split("|")[1],
            "ltp": val.get("last_price"),
            "volume": val.get("volume")
        })

    df = pd.DataFrame(rows)

    if df.empty:
        raise Exception("❌ DataFrame empty")

    return df
