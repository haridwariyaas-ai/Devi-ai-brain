import requests
import os

def get_upstox_price():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    print("🔑 TOKEN:", token)

    if not token:
        print("❌ Token missing")
        return None

    url = "https://api.upstox.com/v2/market-quote/ltp"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # ✅ Try both instruments (fallback logic)
    instruments = [
        "NSE_INDEX|Nifty 50",
        "NSE_INDEX|Nifty Bank"
    ]

    for instrument in instruments:

        params = {
            "instrument_key": instrument
        }

        try:
            response = requests.get(url, headers=headers, params=params)

            print("📡 STATUS CODE:", response.status_code)

            data = response.json()

            print(f"📊 RESPONSE for {instrument}:", data)

            if "data" in data and instrument in data["data"]:
                price = data["data"][instrument]["last_price"]

                print(f"✅ PRICE FOUND ({instrument}):", price)

                return price

        except Exception as e:
            print("❌ ERROR:", e)

    print("⚠️ No valid data from Upstox")

    return None
