import requests
import os
from datetime import datetime, timedelta

# 🔥 AUTO EXPIRY (NEXT THURSDAY)
def get_next_expiry():

    today = datetime.now()

    # Thursday = 3
    days_ahead = 3 - today.weekday()

    if days_ahead <= 0:
        days_ahead += 7

    expiry = today + timedelta(days=days_ahead)

    return expiry.strftime("%d%b").upper()


def get_upstox_oi(price):

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # 🔥 ATM STRIKE
    atm = round(price / 50) * 50

    # 🔥 AUTO EXPIRY
    expiry = get_next_expiry()

    # 🔥 SYMBOLS
    ce_symbol = f"NSE_FO|NIFTY{expiry}{atm}CE"
    pe_symbol = f"NSE_FO|NIFTY{expiry}{atm}PE"

    print("🎯 SYMBOL:", ce_symbol, pe_symbol)

    url = "https://api.upstox.com/v2/market-quote/quotes"

    params = {
        "instrument_key": f"{ce_symbol},{pe_symbol}"
    }

    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()

        if "data" not in data:
            print("❌ BAD RESPONSE:", data)
            return {"call_oi": 0, "put_oi": 0}

        call_oi = data["data"].get(ce_symbol, {}).get("oi", 0)
        put_oi = data["data"].get(pe_symbol, {}).get("oi", 0)

        print("✅ OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ ERROR:", e)

    return {"call_oi": 0, "put_oi": 0}
