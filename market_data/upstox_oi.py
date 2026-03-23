import requests
import os


def get_upstox_oi(price):

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    if not token:
        print("❌ Token missing")
        return {"CE_OI": 0, "PE_OI": 0, "strike": 0}

    try:
        strike = round(price / 50) * 50
    except:
        return {"CE_OI": 0, "PE_OI": 0, "strike": 0}

    ce_key = f"NSE_FO|NIFTY{strike}CE"
    pe_key = f"NSE_FO|NIFTY{strike}PE"

    url = "https://api.upstox.com/v2/market-quote/quotes"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "instrument_key": f"{ce_key},{pe_key}"
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        data = r.json()
    except Exception as e:
        print("❌ API ERROR:", e)
        return {"CE_OI": 0, "PE_OI": 0, "strike": strike}

    # 🔍 DEBUG
    print("OI RAW:", data)

    # ✅ MAIN FIX (CRASH STOPPER)
    if "data" not in data or not data["data"]:
        print("⚠️ EMPTY OI DATA → WRONG SYMBOL (expiry missing)")
        return {
            "CE_OI": 0,
            "PE_OI": 0,
            "strike": strike
        }

    # ✅ SAFE ACCESS (NO KEYERROR)
    ce_data = data["data"].get(ce_key)
    pe_data = data["data"].get(pe_key)

    return {
        "CE_OI": ce_data.get("oi", 0) if ce_data else 0,
        "PE_OI": pe_data.get("oi", 0) if pe_data else 0,
        "strike": strike
    }
