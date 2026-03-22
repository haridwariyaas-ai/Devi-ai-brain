import pandas as pd
import requests
import os

def get_upstox_oi(price):

    try:
        # 🔥 LOAD CSV
        df = pd.read_csv("data/NSE_FO.csv")

        print("📊 CSV LOADED:", len(df))

        # 🔥 ONLY NIFTY OPTIONS (FIXED)
        df = df[df["tradingsymbol"].str.contains("NIFTY", na=False)]

        print("📊 AFTER NIFTY FILTER:", len(df))

        # 🔥 CONVERT EXPIRY
        df["expiry"] = pd.to_datetime(df["expiry"], errors="coerce")

        # 🔥 REMOVE INVALID
        df = df.dropna(subset=["expiry"])

        # 🔥 ONLY FUTURE EXPIRY
        today = pd.Timestamp.today()
        df = df[df["expiry"] >= today]

        print("📊 FUTURE CONTRACTS:", len(df))

        if df.empty:
            print("❌ NO FUTURE DATA")
            return {"call_oi": 0, "put_oi": 0}

        # 🔥 NEAREST EXPIRY
        nearest_expiry = df["expiry"].min()
        df = df[df["expiry"] == nearest_expiry]

        print("📅 EXPIRY:", nearest_expiry)

        # 🔥 ATM STRIKE
        atm = round(price / 50) * 50

        # 🔥 ENSURE STRIKE COLUMN EXISTS
        if "strike" not in df.columns:
            print("❌ STRIKE COLUMN MISSING")
            return {"call_oi": 0, "put_oi": 0}

        # 🔥 CLOSEST STRIKE
        df["diff"] = abs(df["strike"] - atm)
        atm_strike = df.sort_values("diff").iloc[0]["strike"]

        df = df[df["strike"] == atm_strike]

        print("🎯 ATM STRIKE:", atm_strike)

        # 🔥 CE / PE
        ce_df = df[df["option_type"] == "CE"]
        pe_df = df[df["option_type"] == "PE"]

        if ce_df.empty or pe_df.empty:
            print("❌ CE/PE NOT FOUND")
            return {"call_oi": 0, "put_oi": 0}

        ce_row = ce_df.iloc[0]
        pe_row = pe_df.iloc[0]

        ce_key = ce_row["instrument_key"]
        pe_key = pe_row["instrument_key"]

        print("🎯 KEYS:", ce_key, pe_key)

        # 🔥 FETCH OI
        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        url = "https://api.upstox.com/v2/market-quote/quotes"

        params = {
            "instrument_key": f"{ce_key},{pe_key}"
        }

        r = requests.get(url, headers=headers, params=params)
        data = r.json()

        print("📡 API RESPONSE:", data)

        if "data" not in data:
            print("❌ INVALID API RESPONSE")
            return {"call_oi": 0, "put_oi": 0}

        call_oi = data["data"].get(ce_key, {}).get("oi", 0)
        put_oi = data["data"].get(pe_key, {}).get("oi", 0)

        print("✅ FINAL OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ ERROR:", e)

    return {"call_oi": 0, "put_oi": 0}
