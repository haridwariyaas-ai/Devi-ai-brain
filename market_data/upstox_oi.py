import requests
import os

def get_upstox_oi(price):

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # 🔥 STEP 1 — fetch all option contracts
    url = "https://api.upstox.com/v2/option/contract"

    params = {
        "instrument_key": "NSE_INDEX|Nifty 50"
    }

    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        contracts = data.get("data", [])

        if not contracts:
            print("❌ NO CONTRACTS")
            return {"call_oi": 0, "put_oi": 0}

        # 🔥 STEP 2 — ATM strike
        atm = round(price / 50) * 50

        ce_key = None
        pe_key = None

        for c in contracts:

            if c["strike_price"] == atm:

                if c["option_type"] == "CE":
                    ce_key = c["instrument_key"]

                elif c["option_type"] == "PE":
                    pe_key = c["instrument_key"]

        print("🎯 REAL KEYS:", ce_key, pe_key)

        if not ce_key or not pe_key:
            print("❌ KEYS NOT FOUND")
            return {"call_oi": 0, "put_oi": 0}

        # 🔥 STEP 3 — fetch OI using real keys
        quote_url = "https://api.upstox.com/v2/market-quote/quotes"

        params = {
            "instrument_key": f"{ce_key},{pe_key}"
        }

        res = requests.get(quote_url, headers=headers, params=params)
        quote_data = res.json()

        call_oi = quote_data["data"][ce_key].get("oi", 0)
        put_oi = quote_data["data"][pe_key].get("oi", 0)

        print("✅ FINAL OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ ERROR:", e)

    return {"call_oi": 0, "put_oi": 0}
