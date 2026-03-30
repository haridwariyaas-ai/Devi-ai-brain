import requests
import os
from datetime import datetime, timedelta

def get_oi_data(price):
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token or price == 0:
            return {"strike": 0, "call_oi": 0, "put_oi": 0}

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # =========================
        # 🔥 STEP 1: GET EXPIRY (NEXT THURSDAY)
        # =========================
        today = datetime.now()
        days_ahead = 3 - today.weekday()  # Thursday = 3
        if days_ahead <= 0:
            days_ahead += 7

        expiry = today + timedelta(days=days_ahead)
        expiry_str = expiry.strftime("%Y-%m-%d")

        # =========================
        # 🔥 STEP 2: OPTION CHAIN
        # =========================
        url = "https://api.upstox.com/v2/option/chain"

        params = {
            "instrument_key": "NSE_INDEX|Nifty 50",
            "expiry_date": expiry_str
        }

        res = requests.get(url, headers=headers, params=params).json()

        print("📡 OPTION CHAIN:", res)

        if res.get("status") != "success":
            return {"strike": 0, "call_oi": 0, "put_oi": 0}

        chain = res.get("data", [])

        if not chain:
            return {"strike": 0, "call_oi": 0, "put_oi": 0}

        # =========================
        # 🔥 STEP 3: ATM
        # =========================
        atm = int(round(price / 50) * 50)

        closest = min(
            chain,
            key=lambda x: abs(int(x["strike_price"]) - atm)
        )

        strike = int(closest["strike_price"])

        ce_symbol = closest["call_options"]["instrument_key"]
        pe_symbol = closest["put_options"]["instrument_key"]

        print("🎯 STRIKE:", strike)
        print("CE:", ce_symbol)
        print("PE:", pe_symbol)

        # =========================
        # 🔥 STEP 4: QUOTES (OI)
        # =========================
        quote_url = "https://api.upstox.com/v2/market-quote/quotes"

        qparams = {
            "symbol": f"{ce_symbol},{pe_symbol}"
        }

        qres = requests.get(quote_url, headers=headers, params=qparams).json()

        print("📡 QUOTES:", qres)

        data = qres.get("data", {})

        ce_data = None
        pe_data = None

        for k, v in data.items():
            if "CE" in k.upper():
                ce_data = v
            elif "PE" in k.upper():
                pe_data = v

        return {
            "strike": strike,
            "call_oi": ce_data.get("oi", 0) if ce_data else 0,
            "put_oi": pe_data.get("oi", 0) if pe_data else 0
        }

    except Exception as e:
        print("ERROR:", e)
        return {"strike": 0, "call_oi": 0, "put_oi": 0}
