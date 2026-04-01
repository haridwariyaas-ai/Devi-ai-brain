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
        # ✅ ATM
        # =========================
        atm = int(round(float(price) / 50) * 50)
        print("🎯 ATM:", atm)

        # =========================
        # LOAD CSV
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

        df["strike"] = df["strike"].astype(float).astype(int)
        df["option_type"] = df["tradingsymbol"].str[-2:]

        # =========================
        # 🔥 STEP 1: SPLIT CE / PE
        # =========================
        ce_df = df[df["option_type"] == "CE"].copy()
        pe_df = df[df["option_type"] == "PE"].copy()

        # =========================
        # 🔥 STEP 2: COMMON STRIKES
        # =========================
        common_strikes = set(ce_df["strike"]).intersection(set(pe_df["strike"]))

        if not common_strikes:
            return {"strike": 0, "call_oi": 0, "put_oi": 0}

        # =========================
        # 🔥 STEP 3: NEAREST STRIKE (SAFE)
        # =========================
        closest_strike = min(common_strikes, key=lambda x: abs(x - atm))

        print("✅ FINAL STRIKE:", closest_strike)

        ce = ce_df[ce_df["strike"] == closest_strike].iloc[0]
        pe = pe_df[pe_df["strike"] == closest_strike].iloc[0]

        ce_key = ce["instrument_key"]
        pe_key = pe["instrument_key"]

        # =========================
        # 🔥 OI FETCH
        # =========================
        url = "https://api.upstox.com/v2/market-quote/quotes"

        params = {
            "symbol": f"{ce_key},{pe_key}"
        }

        res = requests.get(url, headers=headers, params=params).json()

        print("📡 RESPONSE:", res)

        if res.get("status") != "success":
            return {"strike": closest_strike, "call_oi": 0, "put_oi": 0}

        data = res.get("data", {})

        ce_data = None
        pe_data = None

        for k, v in data.items():
            if "CE" in k.upper():
                ce_data = v
            elif "PE" in k.upper():
                pe_data = v

        return {
            "strike": closest_strike,
            "call_oi": ce_data.get("oi", 0) if ce_data else 0,
            "put_oi": pe_data.get("oi", 0) if pe_data else 0
        }

    except Exception as e:
        print("ERROR:", e)
        return {"strike": 0, "call_oi": 0, "put_oi": 0}
