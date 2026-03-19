import requests
import os

def get_real_oi(price):

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    if not token:
        print("❌ TOKEN MISSING")
        return {"call_oi": 0, "put_oi": 0}

    # 🔥 STEP 1 — ATM CALCULATION
    atm = round(price / 50) * 50

    # ⚠️ IMPORTANT: expiry update karna padega (example)
    expiry = "24MAR"

    ce_symbol = f"NSE_FO|NIFTY{expiry}{atm}CE"
    pe_symbol = f"NSE_FO|NIFTY{expiry}{atm}PE"

    print("🎯 SYMBOLS:", ce_symbol, pe_symbol)

    url = "https://api.upstox.com/v2/market-quote/quotes"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    params = {
        "instrument_key": f"{ce_symbol},{pe_symbol}"
    }

    try:
        r = requests.get(url, headers=headers, params=params)

        print("📡 STATUS:", r.status_code)
        print("📡 RESPONSE:", r.text)

        data = r.json()

        call_oi = 0
        put_oi = 0

        for key in data.get("data", {}):
            item = data["data"][key]

            if "CE" in key:
                call_oi = item.get("oi", 0)

            elif "PE" in key:
                put_oi = item.get("oi", 0)

        print("✅ OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ ERROR:", e)

    return {"call_oi": 0, "put_oi": 0}
