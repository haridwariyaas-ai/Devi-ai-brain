import pandas as pd
import requests
import os

print("🔥 upstox_oi.py loaded")

def get_oi_data(price):
    try:
        print("🚀 OI FUNCTION STARTED")

        if price == 0:
            print("❌ Price is 0")
            return {"call_oi": 0, "put_oi": 0}

        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token:
            print("❌ TOKEN MISSING")
            return {"call_oi": 0, "put_oi": 0}

        atm = round(price / 50) * 50
        print("🎯 ATM:", atm)

        # 🔥 Load CSV
        df = pd.read_csv("data/NSE_FO.csv")
        print("📊 CSV LOADED:", len(df))

        # 🔥 Filter NIFTY
        df = df[df["name"] == "NIFTY"]

        # 🔥 Convert expiry
        df["expiry"] = pd.to_datetime(df["expiry"])

        # 🔥 Nearest expiry
        nearest_expiry = df["expiry"].min()
        print("📅 EXPIRY:", nearest_expiry)

        df = df[df["expiry"] == nearest_expiry]

        # 🔥 ATM filter
        ce_df = df[(df["strike"] == atm) & (df["option_type"] == "CE")]
        pe_df = df[(df["strike"] == atm) & (df["option_type"] == "PE")]

        print("📊 CE FOUND:", len(ce_df))
        print("📊 PE FOUND:", len(pe_df))

        if ce_df.empty or pe_df.empty:
            print("❌ NO STRIKE FOUND")
            return {"call_oi": 0, "put_oi": 0}

        ce_key = ce_df.iloc[0]["instrument_key"]
        pe_key = pe_df.iloc[0]["instrument_key"]

        print("🎯 KEYS:", ce_key, pe_key)

        # 🔥 API CALL
        url = "https://api.upstox.com/v2/market-quote/quotes"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "instrument_key": f"{ce_key},{pe_key}"
        }

        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        print("📡 OI API RESPONSE:", data)

        if data.get("status") != "success":
            print("❌ API FAILED")
            return {"call_oi": 0, "put_oi": 0}

        call_data = data["data"].get(ce_key, {})
        put_data = data["data"].get(pe_key, {})

        call_oi = call_data.get("oi")
        put_oi = put_data.get("oi")

        print("📊 FINAL OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi or 0,
            "put_oi": put_oi or 0
        }

    except Exception as e:
        print("❌ ERROR:", e)
        return {"call_oi": 0, "put_oi": 0}
