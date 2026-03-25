import requests
import os

def get_nifty_price():
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token:
            print("❌ Token missing")
            return 0

        url = "https://api.upstox.com/v2/market-quote/ltp"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "instrument_key": "NSE_INDEX|Nifty 50"
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if "data" not in data:
            print("❌ API failed")
            return 0

        price = data["data"]["NSE_INDEX|Nifty 50"]["last_price"]
        return price

    except Exception as e:
        print("Error:", e)
        return 0
