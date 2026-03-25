import pandas as pd
import requests
import os

print("🔥 upstox_oi.py loaded")

def get_oi_data(price):
    try:
        if price == 0:
            return {"call_oi": 0, "put_oi": 0}

        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token:
            print("❌ TOKEN MISSING")
            return {"call_oi": 0, "put_oi": 0}

        # ATM calculation
        atm = round(price / 50) * 50
        print("🎯 ATM:", atm)

        # Load CSV
        df = pd.read_csv("data/NSE_FO.csv")

        ce_df = df[(df["strike"] == atm) & (df["option_type"] == "CE")]
        pe_df = df[(df["strike"] == atm) & (df["option_type"] == "PE")]

        if ce_df.empty or pe_df.empty:
            print("❌ No matching strike found")
            return {"call_oi": 0, "put_oi": 0}

        ce_key = ce_df.iloc[0]["instrument_key"]
        pe_key = pe_df.iloc[0]["instrument_key"]

        print("🎯 KEYS:", ce_key, pe_key)

        url = "https://api.upstox.com/v2/market-quote/quotes"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "instrument_key": f"{ce_key},{pe_key}"
        }

        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        print("📡 OI API:", data)

        if data.get("status") != "success":
            print("❌ OI API FAILED")
            return {"call_oi": 0, "put_oi": 0}

        call_data = data["data"].get(ce_key, {})
        put_data = data["data"].get(pe_key, {})

        call_oi = call_data.get("oi") or 0
        put_oi = put_data.get("oi") or 0

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ ERROR:", e)
        return {"call_oi": 0, "put_oi": 0}
