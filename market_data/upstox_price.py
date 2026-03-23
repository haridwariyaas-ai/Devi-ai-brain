import requests
import os

def get_nifty_ltp():
    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    url = "https://api.upstox.com/v2/market-quote/ltp"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "instrument_key": "NSE_INDEX|Nifty 50"
    }

    r = requests.get(url, headers=headers, params=params).json()

    if "data" not in r:
        print("PRICE ERROR:", r)
        return 0

    return list(r["data"].values())[0]["last_price"]
