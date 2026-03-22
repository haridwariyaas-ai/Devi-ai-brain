import requests
import os

def get_upstox_oi():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # 🔥 MANUAL VERIFIED KEYS (example)
    ce_key = "NSE_FO|123456"
    pe_key = "NSE_FO|654321"

    url = "https://api.upstox.com/v2/market-quote/quotes"

    params = {
        "instrument_key": f"{ce_key},{pe_key}"
    }

    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()

        call_oi = data["data"][ce_key].get("oi", 0)
        put_oi = data["data"][pe_key].get("oi", 0)

        print("✅ OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except:
        return {"call_oi": 0, "put_oi": 0}
