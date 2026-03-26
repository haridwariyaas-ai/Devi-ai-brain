import requests
import os
from datetime import datetime, timedelta

print("🔥 upstox_oi FINAL FIXED loaded")

def get_oi_data(price):
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token or price == 0:
            return {"call_oi": 0, "put_oi": 0}

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # 🔥 STEP 1: guess nearest expiry (Thursday logic)
        today = datetime.now()

        # next Thursday
        days_ahead = 3 - today.weekday()  # Thursday = 3
        if days_ahead <= 0:
            days_ahead += 7

        expiry = today + timedelta(days=days_ahead)
        expiry_str = expiry.strftime("%Y-%m-%d")

        print("📅 EXPIRY USED:", expiry_str)

        # 🔥 STEP 2: OPTION CHAIN API
        url = "https://api.upstox.com/v2/option/chain"

        params = {
            "instrument_key": "NSE_INDEX|Nifty 50",
            "expiry_date": expiry_str   # ✅ FIX
        }

        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        print("📡 OPTION CHAIN:", data)

        if data.get("status") != "success":
            return {"call_oi": 0, "put_oi": 0}

        options = data.get("data", [])

        if not options:
            return {"call_oi": 0, "put_oi": 0}

        # 🔥 ATM
        atm = round(price / 50) * 50

        closest = min(
            options,
            key=lambda x: abs(int(x["strike_price"]) - atm)
        )

        return {
            "call_oi": closest.get("call_options", {}).get("oi", 0),
            "put_oi": closest.get("put_options", {}).get("oi", 0)
        }

    except Exception as e:
        print("❌ ERROR:", e)
        return {"call_oi": 0, "put_oi": 0}
