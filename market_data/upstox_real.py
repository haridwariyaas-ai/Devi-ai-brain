import requests
import os

def get_upstox_price():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    url = "https://api.upstox.com/v2/market-quote/quotes"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "instrument_key": "NSE_INDEX|Nifty 50"
    }

    r = requests.get(url, headers=headers, params=params)

    data = r.json()

    price = data["data"]["NSE_INDEX:Nifty 50"]["last_price"]

    return price
