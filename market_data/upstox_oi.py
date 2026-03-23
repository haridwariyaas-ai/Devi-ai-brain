import requests
import os

def get_upstox_oi(price):

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    if not token:
        return {"CE_OI": 0, "PE_OI": 0, "strike": 0}

    strike = round(price / 50) * 50

    ce_key = f"NSE_FO|NIFTY{strike}CE"
    pe_key = f"NSE_FO|NIFTY{strike}PE"

    url = "https://api.upstox.com/v2/market-quote/quotes"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "instrument_key": f"{ce_key},{pe_key}"
    }

    r = requests.get(url, headers=headers, params=params).json()

    print("OI RAW:", r)

    # ✅ CRASH FIX
    if "data" not in r or not r["data"]:
        return {
            "CE_OI": 0,
            "PE_OI": 0,
            "strike": strike,
            "error": "Invalid instrument (expiry missing)"
        }

    ce_data = r["data"].get(ce_key)
    pe_data = r["data"].get(pe_key)

    return {
        "CE_OI": ce_data.get("oi", 0) if ce_data else 0,
        "PE_OI": pe_data.get("oi", 0) if pe_data else 0,
        "strike": strike
    }
