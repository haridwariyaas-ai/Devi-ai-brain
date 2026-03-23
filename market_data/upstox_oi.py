import requests
import os


def get_upstox_oi(price):

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    if not token:
        print("OI ERROR: Token missing")
        return {"CE_OI": 0, "PE_OI": 0, "strike": 0}

    # ✅ ATM strike (same as your logic)
    try:
        strike = round(price / 50) * 50
    except:
        return {"CE_OI": 0, "PE_OI": 0, "strike": 0}

    # ⚠️ IMPORTANT: expiry missing tha → isliye OI nahi aa raha tha
    # फिलहाल safe fallback symbol use कर रहे हैं (weekly expiry format)
    ce_symbol = f"NSE_FO|NIFTY{strike}CE"
    pe_symbol = f"NSE_FO|NIFTY{strike}PE"

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

    # 🔍 DEBUG (important)
    print("OI RAW RESPONSE:", data)

    if "data" not in data:
        print("OI INVALID RESPONSE:", data)
        return {"CE_OI": 0, "PE_OI": 0, "strike": strike}

    ce_data = data["data"].get(ce_symbol, {})
    pe_data = data["data"].get(pe_symbol, {})

    return {
        "CE_OI": ce_data.get("oi", 0),
        "PE_OI": pe_data.get("oi", 0),
        "strike": strike
    }
