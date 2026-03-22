import json
import requests
import os

def get_upstox_oi(price):

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    try:
        with open("data/instruments.json") as f:
            data = json.load(f)

        contracts = data.get("data", [])

        if not contracts:
            print("❌ EMPTY CONTRACTS")
            return {"call_oi": 0, "put_oi": 0}

        atm = round(price / 50) * 50

        # 🔥 FIND NEAREST STRIKE
        closest = min(contracts, key=lambda x: abs(x.get("strike_price", 0) - atm))
        atm = closest.get("strike_price")

        print("🎯 ATM:", atm)

        ce_key = None
        pe_key = None

        for c in contracts:

            if c.get("strike_price") == atm:

                if c.get("instrument_type") == "CE":
                    ce_key = c.get("instrument_key")

                elif c.get("instrument_type") == "PE":
                    pe_key = c.get("instrument_key")

        print("🎯 AUTO KEYS:", ce_key, pe_key)

        if not ce_key or not pe_key:
            print("❌ KEYS NOT FOUND")
            return {"call_oi": 0, "put_oi": 0}

        # 🔥 SAFE API CALL
        url = "https://api.upstox.com/v2/market-quote/quotes"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "instrument_key": f"{ce_key},{pe_key}"
        }

        r = requests.get(url, headers=headers, params=params)
        q = r.json()

        if "data" not in q:
            print("❌ INVALID RESPONSE:", q)
            return {"call_oi": 0, "put_oi": 0}

        call_oi = q["data"].get(ce_key, {}).get("oi", 0)
        put_oi = q["data"].get(pe_key, {}).get("oi", 0)

        print("✅ FINAL OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ ERROR:", e)

    return {"call_oi": 0, "put_oi": 0}
