import requests
import os

def get_upstox_price():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    print("🔑 TOKEN:", token)

    if not token:
        print("❌ TOKEN NOT FOUND")
        return None

    url = "https://api.upstox.com/v2/market-quote/ltp"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    params = {
        "instrument_key": "NSE_INDEX|Nifty 50"
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        print("📡 STATUS:", response.status_code)
        print("📡 RAW TEXT:", response.text)

        data = response.json()

        print("📊 JSON:", data)

        if "data" in data and "NSE_INDEX|Nifty 50" in data["data"]:
            price = data["data"]["NSE_INDEX|Nifty 50"]["last_price"]

            print("✅ REAL PRICE:", price)

            return price

        else:
            print("❌ DATA FORMAT ISSUE")

    except Exception as e:
        print("❌ ERROR:", e)

    return None
