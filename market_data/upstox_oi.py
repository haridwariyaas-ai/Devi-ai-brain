import requests
import os


def get_upstox_oi(price):

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    if not token:
        print("❌ TOKEN MISSING")
        return {"call_oi": 0, "put_oi": 0}

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # 🔥 STEP 1 — ATM strike
    atm = round(price / 50) * 50

    # ⚠️ IMPORTANT: expiry must be correct weekly expiry
    expiry = "25SEP"   # 👉 isko baad me auto karenge

    ce = f"NSE_FO|NIFTY{expiry}{atm}CE"
    pe = f"NSE_FO|NIFTY{expiry}{atm}PE"

    print("🎯 SYMBOL:", ce, pe)

    url = "https://api.upstox.com/v2/market-quote/quotes"

    params = {
        "instrument_key": f"{ce},{pe}"
    }

    try:
        r = requests.get(url, headers=headers, params=params)

        print("📡 STATUS:", r.status_code)
        print("📡 RESPONSE:", r.text)

        data = r.json()

        call_oi = 0
        put_oi = 0

        for key, val in data.get("data", {}).items():

            if key == ce:
                call_oi = val.get("oi", 0)

            elif key == pe:
                put_oi = val.get("oi", 0)

        print("✅ OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ ERROR:", e)

    return {"call_oi": 0, "put_oi": 0}
