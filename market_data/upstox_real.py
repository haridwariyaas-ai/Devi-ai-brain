import requests
import os

def get_nifty_price():
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        url = "https://api.upstox.com/v2/market-quote/ltp"
        params = {"instrument_key": "NSE_INDEX|Nifty 50"}

        r = requests.get(url, headers=headers, params=params).json()

        if r.get("status") != "success":
            return 0

        key = list(r["data"].keys())[0]
        return r["data"][key]["last_price"]

    except:
        return 0
