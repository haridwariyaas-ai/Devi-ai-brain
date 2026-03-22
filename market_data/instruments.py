import requests
import os
import json

def download_instruments():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # 🔥 CORRECT ENDPOINT
    url = "https://api.upstox.com/v2/instruments"

    params = {
        "segment": "NSE_FO"
    }

    r = requests.get(url, headers=headers, params=params)

    data = r.json()

    if "data" not in data:
        print("❌ FAILED TO FETCH INSTRUMENTS:", data)
        return

    # 🔥 FILTER ONLY NIFTY OPTIONS
    filtered = []

    for item in data["data"]:

        if "NIFTY" in item.get("trading_symbol", ""):
            filtered.append(item)

    with open("data/instruments.json", "w") as f:
        json.dump({"data": filtered}, f)

    print("✅ Instruments saved:", len(filtered))
