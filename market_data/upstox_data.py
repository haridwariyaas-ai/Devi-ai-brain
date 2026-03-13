import requests
import os

def get_nifty_price():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    if not token:
        print("Token missing")
        return None

    url = "https://api.upstox.com/v2/market-quote/ltp"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "instrument_key": "NSE_INDEX|Nifty 50"
    }

    r = requests.get(url, headers=headers, params=params)

    data = r.json()

    if "data" in data and "NSE_INDEX|Nifty 50" in data["data"]:
        return data["data"]["NSE_INDEX|Nifty 50"]["last_price"]

    return None
