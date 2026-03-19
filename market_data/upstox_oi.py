import requests
import os
from datetime import datetime


def get_real_oi(price):

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    if not token:
        print("❌ TOKEN MISSING")
        return {"call_oi": 0, "put_oi": 0}

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # 🔥 STEP 1 — Get instruments (NIFTY options)
    url = "https://api.upstox.com/v2/option/contract"

    params = {
        "instrument_key": "NSE_INDEX|Nifty 50"
    }

    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        contracts = data.get("data", [])

        if not contracts:
            print("❌ No contracts found")
            return {"call_oi": 0, "put_oi": 0}

        # 🔥 STEP 2 — Find nearest expiry
        today = datetime.now().date()

        expiries = sorted(list(set([c["expiry"] for c in contracts])))

        nearest_expiry = None

        for exp in expiries:
            exp_date = datetime.strptime(exp, "%Y-%m-%d").date()
            if exp_date >= today:
                nearest_expiry = exp
                break

        print("📅 NEAREST EXPIRY:", nearest_expiry)

        # 🔥 STEP 3 — ATM strike
        atm = round(price / 50) * 50

        # 🔥 STEP 4 — Find matching CE & PE
        ce = None
        pe = None

        for c in contracts:
            if c["expiry"] == nearest_expiry and c["strike_price"] == atm:

                if c["option_type"] == "CE":
                    ce = c["instrument_key"]

                elif c["option_type"] == "PE":
                    pe = c["instrument_key"]

        print("🎯 CE:", ce)
        print("🎯 PE:", pe)

        if not ce or not pe:
            print("❌ ATM instruments not found")
            return {"call_oi": 0, "put_oi": 0}

        # 🔥 STEP 5 — Fetch OI
        quote_url = "https://api.upstox.com/v2/market-quote/quotes"

        params = {
            "instrument_key": f"{ce},{pe}"
        }

        res = requests.get(quote_url, headers=headers, params=params)
        quote_data = res.json()

        call_oi = 0
        put_oi = 0

        for key, val in quote_data.get("data", {}).items():

            if key == ce:
                call_oi = val.get("oi", 0)

            elif key == pe:
                put_oi = val.get("oi", 0)

        print("✅ FINAL OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ ERROR:", e)

    return {"call_oi": 0, "put_oi": 0}
