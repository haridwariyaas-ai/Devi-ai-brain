import requests
import os

print("🔥 upstox_real loaded")

def get_nifty_price():
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token:
            return 0

        url = "https://api.upstox.com/v2/market-quote/ltp"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "instrument_key": "NSE_INDEX|Nifty 50"
        }

        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        if data.get("status") != "success":
            return 0

        key = list(data["data"].keys())[0]
        return data["data"][key]["last_price"]

    except:
        return 0
