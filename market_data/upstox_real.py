import requests
import os


BASE_URL = "https://api.upstox.com/v2/market-quote/quotes"


def _make_request(instrument_keys):
    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    if not token:
        return {"error": "TOKEN_MISSING"}

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "instrument_key": instrument_keys
    }

    try:
        r = requests.get(BASE_URL, headers=headers, params=params, timeout=5)
        data = r.json()
        return data
    except Exception as e:
        return {"error": str(e)}


# ✅ PRICE FUNCTION (SAFE)
def get_upstox_price():

    data = _make_request("NSE_INDEX|Nifty 50")

    if "data" not in data or not data["data"]:
        print("PRICE API ERROR:", data)
        return 0  # fallback

    key = list(data["data"].keys())[0]

    return data["data"][key].get("last_price", 0)


# ✅ OI FUNCTION (SAFE + NON-BREAKING)
def get_upstox_oi(price):

    if price == 0:
        return {"CE_OI": 0, "PE_OI": 0, "strike": 0}

    strike = round(price / 50) * 50

    ce_key = f"NSE_FO|NIFTY{strike}CE"
    pe_key = f"NSE_FO|NIFTY{strike}PE"

    data = _make_request(f"{ce_key},{pe_key}")

    if "data" not in data:
        print("OI API ERROR:", data)
        return {"CE_OI": 0, "PE_OI": 0, "strike": strike}

    ce_data = data["data"].get(ce_key, {})
    pe_data = data["data"].get(pe_key, {})

    return {
        "CE_OI": ce_data.get("oi", 0),
        "PE_OI": pe_data.get("oi", 0),
        "strike": strike
    }
