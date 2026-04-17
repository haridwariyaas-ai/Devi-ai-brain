# data/upstox_data.py

import requests
import pandas as pd
from config import ACCESS_TOKEN

BASE_URL = "https://api.upstox.com/v2/market-quote/quotes"

def get_market_quotes(symbols):
    """
    Fetch live NSE equity quotes from Upstox
    """

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    instrument_keys = [f"NSE_EQ|{symbol}" for symbol in symbols]

    params = {
        "instrument_key": ",".join(instrument_keys)
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Upstox API Error: {response.text}")

    data = response.json()["data"]

    rows = []

    for key, val in data.items():
        rows.append({
            "symbol": key.split("|")[1],
            "ltp": val["last_price"],
            "volume": val["volume"],
            "open": val["ohlc"]["open"],
            "high": val["ohlc"]["high"],
            "low": val["ohlc"]["low"],
            "prev_close": val["ohlc"]["close"]
        })

    return pd.DataFrame(rows)
