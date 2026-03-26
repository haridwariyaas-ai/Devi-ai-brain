import requests
import os

def get_oi_data(price):
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token or price == 0:
            return {"strike": 0, "call_oi": 0, "put_oi": 0}

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # 🔥 STEP 1: GET OPTION CHAIN (WITH EXPIRY)
        url = "https://api.upstox.com/v2/option/chain"

        # 👉 HARDCODE TEMP (WORKING GUARANTEED)
        params = {
            "instrument_key": "NSE_INDEX|Nifty 50",
            "expiry_date": "2026-03-26"   # ⚠️ next Thursday adjust karna later
        }

        res = requests.get(url, headers=headers, params=params).json()

        print("📡 OPTION CHAIN:", res)

        if res.get("status") != "success":
            return {"strike": 0, "call_oi": 0, "put_oi": 0}

        data = res.get("data", [])

        if not data:
            return {"strike": 0, "call_oi": 0, "put_oi": 0}

        # 🔥 STEP 2: ATM
        atm = int(round(price / 50) * 50)

        # 🔥 STEP 3: CLOSEST STRIKE
        closest = min(
            data,
            key=lambda x: abs(int(x["strike_price"]) - atm)
        )

        strike = int(closest["strike_price"])

        call_oi = closest.get("call_options", {}).get("oi", 0)
        put_oi = closest.get("put_options", {}).get("oi", 0)

        return {
            "strike": strike,
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("ERROR:", e)
        return {"strike": 0, "call_oi": 0, "put_oi": 0}
