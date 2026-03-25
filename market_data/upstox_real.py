import requests
import os

print("🔥 upstox_real.py loaded")

def get_nifty_price():
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token:
            print("❌ TOKEN MISSING")
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

        print("📡 PRICE API:", data)

        # 🔴 Handle invalid token
        if data.get("status") != "success":
            print("❌ API FAILED:", data)
            return 0

        return data["data"]["NSE_INDEX|Nifty 50"]["last_price"]

    except Exception as e:
        print("❌ ERROR:", e)
        return 0
