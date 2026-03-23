import pandas as pd
import requests
import os

def get_upstox_oi(price):

    try:
        df = pd.read_csv("data/NSE_FO.csv")

        # 🔥 Only NIFTY
        df = df[df["tradingsymbol"].str.contains("NIFTY", na=False)]

        # 🔥 expiry
        df["expiry"] = pd.to_datetime(df["expiry"], errors="coerce")
        df = df.dropna(subset=["expiry"])

        # 🔥 future expiry only
        today = pd.Timestamp.today()
        df = df[df["expiry"] >= today]

        if df.empty:
            print("❌ NO DATA AFTER EXPIRY FILTER")
            return {"call_oi": 0, "put_oi": 0}

        # 🔥 nearest expiry
        nearest_expiry = df["expiry"].min()
        df = df[df["expiry"] == nearest_expiry]

        # 🔥 ATM
        atm = round(price / 50) * 50

        df["diff"] = abs(df["strike"] - atm)
        atm_strike = df.sort_values("diff").iloc[0]["strike"]

        df = df[df["strike"] == atm_strike]

        # 🔥 CE / PE
        ce = df[df["option_type"] == "CE"].iloc[0]
        pe = df[df["option_type"] == "PE"].iloc[0]

        ce_key = ce["instrument_key"]
        pe_key = pe["instrument_key"]

        print("🎯 KEYS:", ce_key, pe_key)

        # 🔥 API
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

        call_oi = data["data"].get(ce_key, {}).get("oi", 0)
        put_oi = data["data"].get(pe_key, {}).get("oi", 0)

        print("✅ OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ ERROR:", e)

    return {"call_oi": 0, "put_oi": 0}
