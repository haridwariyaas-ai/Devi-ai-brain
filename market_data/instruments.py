import requests
import os
import json

def download_instruments():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    url = "https://api.upstox.com/v2/option/contract"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "instrument_key": "NSE_INDEX|Nifty 50"
    }

    r = requests.get(url, headers=headers, params=params)

    data = r.json()

    with open("data/instruments.json", "w") as f:
        json.dump(data, f)

    print("✅ Instruments saved")
