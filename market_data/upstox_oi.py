import requests
import os

print("🔥 upstox_oi.py loaded")

def get_oi_data(price):
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token or price == 0:
            return {"call_oi": 0, "put_oi": 0}

        atm = round(price / 50) * 50
        print("🎯 ATM:", atm)

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
            return {"call_oi": 0, "put_oi": 0}

        options = data["data"]

        # 🔥 Find ATM strike
        for opt in options:
            if int(opt["strike_price"]) == atm:
                return {
                    "call_oi": opt["call_options"]["oi"],
                    "put_oi": opt["put_options"]["oi"]
                }

        return {"call_oi": 0, "put_oi": 0}

    except Exception as e:
        print("❌ ERROR:", e)
        return {"call_oi": 0, "put_oi": 0}
