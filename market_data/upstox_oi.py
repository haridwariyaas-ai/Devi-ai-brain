import requests
import os
from datetime import datetime, timedelta


# ✅ NEXT THURSDAY FINDER (NIFTY expiry)
def get_next_expiry():
    today = datetime.now()
    days_ahead = 3 - today.weekday()  # Thursday = 3

    if days_ahead <= 0:
        days_ahead += 7

    expiry = today + timedelta(days=days_ahead)

    return expiry.strftime("%d%b").upper()  # e.g. 28MAR


# ✅ MAIN OI FUNCTION
def get_upstox_oi(price):

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    if not token:
        print("OI ERROR: Token missing")
        return {"CE_OI": 0, "PE_OI": 0, "strike": 0}

    try:
        strike = round(price / 50) * 50
    except:
        return {"CE_OI": 0, "PE_OI": 0, "strike": 0}

    expiry = get_next_expiry()

    # ✅ CORRECT SYMBOL FORMAT
    ce_symbol = f"NSE_FO|NIFTY{expiry}{strike}CE"
    pe_symbol = f"NSE_FO|NIFTY{expiry}{strike}PE"

    url = "https://api.upstox.com/v2/market-quote/quotes"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "instrument_key": f"{ce_symbol},{pe_symbol}"
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        data = r.json()
    except Exception as e:
        print("OI API ERROR:", e)
        return {"CE_OI": 0, "PE_OI": 0, "strike": strike}

    # 🔍 DEBUG
    print("OI RAW:", data)

    if "data" not in data:
        print("OI INVALID:", data)
        return {"CE_OI": 0, "PE_OI": 0, "strike": strike}

    ce_data = data["data"].get(ce_symbol, {})
    pe_data = data["data"].get(pe_symbol, {})

    return {
        "CE_OI": ce_data.get("oi", 0),
        "PE_OI": pe_data.get("oi", 0),
        "strike": strike,
        "expiry": expiry
    }
