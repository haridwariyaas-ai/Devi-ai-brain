import requests
import os

def get_upstox_oi(price):

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # 🔥 STEP 1 — fetch option contracts
    url = "https://api.upstox.com/v2/option/contract"

    params = {
        "instrument_key": "NSE_INDEX|Nifty 50"
    }

    r = requests.get(url, headers=headers, params=params)
    data = r.json()

    contracts = data.get("data", [])

    if not contracts:
        print("❌ NO CONTRACT DATA")
        return {"call_oi": 0, "put_oi": 0}

    # 🔥 STEP 2 — nearest expiry
    expiries = sorted(list(set([c["expiry"] for c in contracts])))
    nearest_expiry = expiries[0]

    contracts = [c for c in contracts if c["expiry"] == nearest_expiry]

    # 🔥 STEP 3 — ATM
    atm = round(price / 50) * 50

    closest = min(contracts, key=lambda x: abs(x["strike_price"] - atm))
    atm = closest["strike_price"]

    print("🎯 ATM:", atm)

    ce_key = None
    pe_key = None

    for c in contracts:

        if c["strike_price"] == atm:

            opt = c.get("instrument_type") or c.get("option_type")

            if opt == "CE":
                ce_key = c["instrument_key"]

            elif opt == "PE":
                pe_key = c["instrument_key"]

    print("🎯 KEYS:", ce_key, pe_key)

    if not ce_key or not pe_key:
        print("❌ KEYS NOT FOUND")
        return {"call_oi": 0, "put_oi": 0}

    # 🔥 STEP 4 — fetch OI
    quote_url = "https://api.upstox.com/v2/market-quote/quotes"

    params = {
        "instrument_key": f"{ce_key},{pe_key}"
    }

    r = requests.get(quote_url, headers=headers, params=params)
    q = r.json()

    if "data" not in q:
        print("❌ BAD RESPONSE:", q)
        return {"call_oi": 0, "put_oi": 0}

    call_oi = q["data"][ce_key]["oi"]
    put_oi = q["data"][pe_key]["oi"]

    print("✅ FINAL OI:", call_oi, put_oi)

    return {
        "call_oi": call_oi,
        "put_oi": put_oi
    }
