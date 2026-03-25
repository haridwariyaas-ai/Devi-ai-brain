import pandas as pd
import requests
import os

print("🔥 upstox_oi.py loaded")

def get_oi_data(price):
    try:
        if price == 0:
            print("❌ Price is 0")
            return {"call_oi": 0, "put_oi": 0}

        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token:
            print("❌ Token missing")
            return {"call_oi": 0, "put_oi": 0}

        atm = round(price / 50) * 50
        print("🎯 ATM:", atm)

        df = pd.read_csv("data/NSE_FO.csv")

        ce_df = df[(df["strike"] == atm) & (df["option_type"] == "CE")]
        pe_df = df[(df["strike"] == atm) & (df["option_type"] == "PE")]

        if ce_df.empty or pe_df.empty:
            print("❌ No CE/PE found")
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

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        print("📡 OI API:", data)

        if data.get("status") != "success":
            print("❌ OI API failed")
            return {"call_oi": 0, "put_oi": 0}

        call_oi = data["data"].get(ce_key, {}).get("oi", 0)
        put_oi = data["data"].get(pe_key, {}).get("oi", 0)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ ERROR:", e)
        return {"call_oi": 0, "put_oi": 0}
