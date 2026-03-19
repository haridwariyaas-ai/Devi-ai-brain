import requests
import os

def get_real_oi():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    url = "https://api.upstox.com/v2/market-quote/quotes"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # ⚠️ Example instruments (ATM CE/PE)
    instruments = [
        "NSE_FO|NIFTY24MAR22500CE",
        "NSE_FO|NIFTY24MAR22500PE"
    ]

    params = {
        "instrument_key": ",".join(instruments)
    }

    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()

        call_oi = 0
        put_oi = 0

        for key in data.get("data", {}):
            item = data["data"][key]

            if "CE" in key:
                call_oi = item.get("oi", 0)

            if "PE" in key:
                put_oi = item.get("oi", 0)

        print("✅ REAL OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ OI ERROR:", e)

    return {
        "call_oi": 0,
        "put_oi": 0
    }
