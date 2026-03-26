import requests
import os

print("🔥 upstox_oi FINAL loaded")

def get_oi_data(price):
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token or price == 0:
            return {"call_oi": 0, "put_oi": 0}

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # 🔥 OPTION CHAIN API (CORRECT SOURCE OF OI)
        url = "https://api.upstox.com/v2/option/chain"

        params = {
            "instrument_key": "NSE_INDEX|Nifty 50"
        }

        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        print("📡 OPTION CHAIN:", data)

        if data.get("status") != "success":
            return {"call_oi": 0, "put_oi": 0}

        options = data.get("data", [])

        if not options:
            return {"call_oi": 0, "put_oi": 0}

        # 🔥 ATM STRIKE
        atm = round(price / 50) * 50

        # 🔥 CLOSEST STRIKE
        closest = min(
            options,
            key=lambda x: abs(int(x["strike_price"]) - atm)
        )

        call_oi = closest.get("call_options", {}).get("oi", 0)
        put_oi = closest.get("put_options", {}).get("oi", 0)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ ERROR:", e)
        return {"call_oi": 0, "put_oi": 0}
