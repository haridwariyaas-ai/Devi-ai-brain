import pandas as pd
import requests
import os

print("🔥 FINAL OI FIX LOADED")

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

        df = df[
            (df["exchange"] == "NSE_FO") &
            (df["instrument_type"] == "OPTIDX") &
            (df["tradingsymbol"].str.contains("NIFTY"))
        ].copy()

        df["expiry"] = pd.to_datetime(df["expiry"])
        df = df[df["expiry"] >= pd.Timestamp.today().normalize()]

        nearest_expiry = df["expiry"].min()
        df = df[df["expiry"] == nearest_expiry]

        # 🔥 ATM
        df["diff"] = abs(df["strike"] - price)
        atm = df.sort_values("diff").iloc[0]["strike"]

        df["option_type"] = df["tradingsymbol"].str[-2:]

        ce = df[(df["strike"] == atm) & (df["option_type"] == "CE")].iloc[0]
        pe = df[(df["strike"] == atm) & (df["option_type"] == "PE")].iloc[0]

        ce_key = ce["instrument_key"]
        pe_key = pe["instrument_key"]

        # 🔥 API CALL
        url = "https://api.upstox.com/v2/market-quote/quotes"

        params = {
            "symbol": f"{ce_key},{pe_key}"
        }

        res = requests.get(url, headers=headers, params=params).json()

        print("📡 FINAL RESPONSE:", res)

        data = res.get("data", {})

        # ✅ DIRECT ACCESS (NO MATCHING BUG)
        ce_data = None
        pe_data = None

        for key, value in data.items():
            sym = key.upper()

            if "CE" in sym:
                ce_data = value
            elif "PE" in sym:
                pe_data = value

        if not ce_data or not pe_data:
            return {"call_oi": 0, "put_oi": 0}

        return {
            "call_oi": ce_data.get("oi", 0),
            "put_oi": pe_data.get("oi", 0)
        }

    except Exception as e:
        print("❌ ERROR:", e)
        return {"call_oi": 0, "put_oi": 0}
