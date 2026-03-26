import pandas as pd
import requests
import os

print("🔥 upstox_oi.py loaded")

def get_oi_data(price):
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token or price == 0:
            return {"call_oi": 0, "put_oi": 0}

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # 🔥 LOAD CSV
        df = pd.read_csv("data/NSE_FO.csv")

        # 🔥 FILTER NIFTY
        df = df[
            (df["exchange"] == "NSE_FO") &
            (df["instrument_type"] == "OPTIDX") &
            (df["tradingsymbol"].str.contains("NIFTY"))
        ].copy()

        df["expiry"] = pd.to_datetime(df["expiry"])
        today = pd.Timestamp.today().normalize()

        df = df[df["expiry"] >= today]
        nearest_expiry = df["expiry"].min()
        df = df[df["expiry"] == nearest_expiry]

        # 🔥 ATM STRIKE
        df["strike_diff"] = abs(df["strike"] - price)
        atm_strike = df.sort_values("strike_diff").iloc[0]["strike"]

        # 🔥 CE / PE
        df["option_type"] = df["tradingsymbol"].str[-2:]

        ce_df = df[df["option_type"] == "CE"]
        pe_df = df[df["option_type"] == "PE"]

        ce_df["strike_diff"] = abs(ce_df["strike"] - price)
        pe_df["strike_diff"] = abs(pe_df["strike"] - price)

        atm_ce = ce_df.sort_values("strike_diff").iloc[0]
        atm_pe = pe_df.sort_values("strike_diff").iloc[0]

        ce_key = atm_ce["instrument_key"]
        pe_key = atm_pe["instrument_key"]

        print("🎯 KEYS:", ce_key, pe_key)

        # 🔥 🔥 IMPORTANT FIX HERE 🔥 🔥
        url = "https://api.upstox.com/v2/market-quote/quotes"

        params = {
            "symbol": f"{ce_key},{pe_key}"   # ✅ CORRECT
        }

        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        print("📡 QUOTES API:", data)

        if data.get("status") != "success":
            return {"call_oi": 0, "put_oi": 0}

        quotes = data["data"]

        ce_data = next(v for v in quotes.values() if v["instrument_token"] == ce_key)
        pe_data = next(v for v in quotes.values() if v["instrument_token"] == pe_key)

        return {
            "call_oi": ce_data.get("oi", 0),
            "put_oi": pe_data.get("oi", 0)
        }

    except Exception as e:
        print("❌ ERROR:", e)
        return {"call_oi": 0, "put_oi": 0}
