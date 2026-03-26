import requests
import os

print("🔥 upstox_oi.py loaded")

def get_oi_data(price):
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token:
            print("❌ TOKEN MISSING")
            return {"call_oi": 0, "put_oi": 0}

        url = "https://api.upstox.com/v2/option/chain"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "instrument_key": "NSE_INDEX|Nifty 50"
        }

        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        print("📡 OPTION CHAIN:", data)

        if data.get("status") != "success":
            print("❌ API FAILED")
            return {"call_oi": 0, "put_oi": 0}

        options = data.get("data", [])

        if not options:
            print("❌ NO OPTION DATA")
            return {"call_oi": 0, "put_oi": 0}

        atm = round(price / 50) * 50
        print("🎯 ATM:", atm)

        # 🔥 Find nearest strike
        closest = min(options, key=lambda x: abs(int(x["strike_price"]) - atm))

        call_oi = closest.get("call_options", {}).get("oi", 0)
        put_oi = closest.get("put_options", {}).get("oi", 0)

        print("📊 FINAL OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ ERROR:", e)
        return {"call_oi": 0, "put_oi": 0}
