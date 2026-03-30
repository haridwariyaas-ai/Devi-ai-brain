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
        # ✅ ONLY CHANGE: ATM FIX
        # =========================
        atm = int(round(float(price) / 50) * 50)
        print("🎯 ATM:", atm)

        # =========================
        # SAME WORKING CSV LOGIC
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

        # 🔥 IMPORTANT (ye missing tha pehle)
        df["strike"] = df["strike"].astype(float).astype(int)
        df["option_type"] = df["tradingsymbol"].str[-2:]

        # =========================
        # ⚠️ SAME OLD WORKING MATCH (NO SMARTNESS)
        # =========================
        ce = df[df["option_type"] == "CE"].copy()
        pe = df[df["option_type"] == "PE"].copy()

        ce["diff"] = abs(ce["strike"] - atm)
        pe["diff"] = abs(pe["strike"] - atm)

        atm_ce = ce.sort_values("diff").iloc[0]
        atm_pe = pe.sort_values("diff").iloc[0]

        strike = int(atm_ce["strike"])  # final strike

        print("✅ STRIKE USED:", strike)

        ce_key = atm_ce["instrument_key"]
        pe_key = atm_pe["instrument_key"]

        # =========================
        # SAME WORKING API
        # =========================
        url = "https://api.upstox.com/v2/market-quote/quotes"

        params = {
            "symbol": f"{ce_key},{pe_key}"
        }

        res = requests.get(url, headers=headers, params=params).json()

        print("📡 RESPONSE:", res)

        if res.get("status") != "success":
            return {"strike": strike, "call_oi": 0, "put_oi": 0}

        data = res.get("data", {})

        ce_data = None
        pe_data = None

        for k, v in data.items():
            name = k.upper()

            if "CE" in name:
                ce_data = v
            elif "PE" in name:
                pe_data = v

        return {
            "strike": strike,
            "call_oi": ce_data.get("oi", 0) if ce_data else 0,
            "put_oi": pe_data.get("oi", 0) if pe_data else 0
        }

    except Exception as e:
        print("ERROR:", e)
        return {"strike": 0, "call_oi": 0, "put_oi": 0}
