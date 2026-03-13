import requests
import os

ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def get_nifty_price():

    url = "https://api.upstox.com/v2/market-quote/ltp?instrument_key=NSE_INDEX|Nifty 50"

    r = requests.get(url, headers=headers)

    data = r.json()

    price = data["data"]["NSE_INDEX|Nifty 50"]["last_price"]

    return price
