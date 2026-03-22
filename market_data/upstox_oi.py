import json
import requests
import os

def get_upstox_oi(price):

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    with open("data/instruments.json") as f:
        data = json.load(f)

    contracts = data.get("data", [])

    atm = round(price / 50) * 50

    ce_key = None
    pe_key = None

    for c in contracts:

        if c["strike_price"] == atm:

            if c["option_type"] == "CE":
                ce_key = c["instrument_key"]

            elif c["option_type"] == "PE":
                pe_key = c["instrument_key"]

    print("🎯 AUTO KEYS:", ce_key, pe_key)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = "https://api.upstox.com/v2/market-quote/quotes"

    params = {
        "instrument_key": f"{ce_key},{pe_key}"
    }

    r = requests.get(url, headers=headers, params=params)

    q = r.json()

    call_oi = q["data"][ce_key].get("oi", 0)
    put_oi = q["data"][pe_key].get("oi", 0)

    print("✅ OI:", call_oi, put_oi)

    return {
        "call_oi": call_oi,
        "put_oi": put_oi
    }
