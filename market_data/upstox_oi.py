import requests
import os

def get_option_oi(ce_key, pe_key):

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    url = "https://api.upstox.com/v2/market-quote/quotes"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "instrument_key": f"{ce_key},{pe_key}"
    }

    r = requests.get(url, headers=headers, params=params).json()

    if "data" not in r:
        print("OI ERROR:", r)
        return {"CE_OI": 0, "PE_OI": 0}

    quotes = r["data"]

    ce_data = next(v for v in quotes.values() if v["instrument_token"] == ce_key)
    pe_data = next(v for v in quotes.values() if v["instrument_token"] == pe_key)

    return {
        "CE_OI": ce_data.get("oi", 0),
        "PE_OI": pe_data.get("oi", 0)
    }
