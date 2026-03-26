import requests
import os

def get_oi_data(price):
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token:
            return {"call_oi": 0, "put_oi": 0}

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        url = "https://api.upstox.com/v2/option/chain"
        params = {
            "instrument_key": "NSE_INDEX|Nifty 50"
        }

        res = requests.get(url, headers=headers, params=params).json()

        print("📡 OPTION CHAIN RAW:", res)

        if res.get("status") != "success":
            return {"call_oi": 0, "put_oi": 0}

        data = res.get("data", [])

        if not data:
            return {"call_oi": 0, "put_oi": 0}

        # 🔥 ATM calculation
        atm = round(price / 50) * 50

        # 🔥 nearest strike
        closest = min(
            data,
            key=lambda x: abs(int(x.get("strike_price", 0)) - atm)
        )

        call_oi = closest.get("call_options", {}).get("oi", 0)
        put_oi = closest.get("put_options", {}).get("oi", 0)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("ERROR:", e)
        return {"call_oi": 0, "put_oi": 0}
