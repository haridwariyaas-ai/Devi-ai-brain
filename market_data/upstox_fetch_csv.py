import requests
import os
import pandas as pd

def fetch_and_save_data():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    print("🔑 TOKEN:", token)

    url = "https://api.upstox.com/v2/market-quote/ltp"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    params = {
        "instrument_key": "NSE_INDEX|Nifty 50"
    }

    try:
        r = requests.get(url, headers=headers, params=params)

        print("📡 STATUS:", r.status_code)
        print("📡 RESPONSE TEXT:", r.text)

        data = r.json()

        if "data" in data and "NSE_INDEX|Nifty 50" in data["data"]:

            price = data["data"]["NSE_INDEX|Nifty 50"]["last_price"]

            df = pd.DataFrame([{"price": price}])
            df.to_csv("data/live_data.csv", index=False)

            print("✅ REAL PRICE:", price)

            return price

        else:
            print("❌ DATA NOT FOUND")

    except Exception as e:
        print("❌ ERROR:", e)

    return None
