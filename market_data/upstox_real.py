import requests
import os

def get_upstox_price():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    print("🔑 TOKEN:", token)

    if not token:
        print("❌ TOKEN MISSING")
        return None

    url = "https://api.upstox.com/v2/market-quote/ltp"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # ✅ Correct instrument (IMPORTANT FIX)
    params = {
        "instrument_key": "NSE_INDEX|Nifty 50"
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        print("📡 STATUS:", response.status_code)
        print("📡 RESPONSE:", response.text)

        if response.status_code != 200:
            return None

        data = response.json()

        # ✅ SAFE EXTRACTION
        if "data" in data:
            for key in data["data"]:
                price = data["data"][key]["last_price"]
                print("✅ REAL PRICE:", price)
                return price

        print("❌ DATA FORMAT ISSUE")

    except Exception as e:
        print("❌ ERROR:", e)

    return None
