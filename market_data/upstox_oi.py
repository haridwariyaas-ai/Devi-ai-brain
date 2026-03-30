import pandas as pd
import requests
import os

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
        # ✅ CORRECT ATM
        # =========================
        atm = int(round(float(price) / 50) * 50)
        print("🎯 ATM:", atm)

        # =========================
        # LOAD CSV (SAME AS WORKING)
        # =========================
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

        # 🔥 IMPORTANT FIX
        df["strike"] = df["strike"].astype(float).astype(int)
        df["option_type"] = df["tradingsymbol"].str[-2:]

        # =========================
        # ✅ EXACT ATM + SAFE FALLBACK
        # =========================
        ce = df[(df["strike"] == atm) & (df["option_type"] == "CE")]
        pe = df[(df["strike"] == atm) & (df["option_type"] == "PE")]

        if ce.empty or pe.empty:
            print("⚠️ ATM not found, using closest")

            df["diff"] = abs(df["strike"] - atm)
            closest = df.sort_values("diff").iloc[0]["strike"]

            ce = df[(df["strike"] == closest) & (df["option_type"] == "CE")]
            pe = df[(df["strike"] == closest) & (df["option_type"] == "PE")]

            atm = int(closest)

        # =========================
        # GET KEYS (IMPORTANT)
        # =========================
        ce_key = ce.iloc[0]["instrument_key"]
        pe_key = pe.iloc[0]["instrument_key"]

        print("🎯 FINAL STRIKE:", atm)
        print("CE KEY:", ce_key)
        print("PE KEY:", pe_key)

        # =========================
        # QUOTES API (WORKING PART)
        # =========================
        url = "https://api.upstox.com/v2/market-quote/quotes"

        params = {
            "symbol": f"{ce_key},{pe_key}"
        }

        res = requests.get(url, headers=headers, params=params).json()

        print("📡 RESPONSE:", res)

        if res.get("status") != "success":
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        data = res.get("data", {})

        # 🔥 SAFE MATCH (THIS WAS WORKING EARLIER)
        ce_data = None
        pe_data = None

        for k, v in data.items():
            name = k.upper()

            if "CE" in name:
                ce_data = v
            elif "PE" in name:
                pe_data = v

        return {
            "strike": atm,
            "call_oi": ce_data.get("oi", 0) if ce_data else 0,
            "put_oi": pe_data.get("oi", 0) if pe_data else 0
        }

    except Exception as e:
        print("ERROR:", e)
        return {"strike": 0, "call_oi": 0, "put_oi": 0}
