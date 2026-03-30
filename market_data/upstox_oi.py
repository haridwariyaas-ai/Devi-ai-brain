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
        # ✅ STEP 1: CORRECT ATM
        # =========================
        atm = int(round(float(price) / 50) * 50)
        print("🎯 IDEAL ATM:", atm)

        # =========================
        # LOAD CSV (WORKING SOURCE)
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
        # ✅ STEP 2: EXACT ATM TRY
        # =========================
        ce = df[(df["strike"] == atm) & (df["option_type"] == "CE")]
        pe = df[(df["strike"] == atm) & (df["option_type"] == "PE")]

        # =========================
        # 🔁 STEP 3: FALLBACK (ONLY IF NEEDED)
        # =========================
        if ce.empty or pe.empty:
            print("⚠️ EXACT ATM NOT FOUND → USING CLOSEST")

            df["diff"] = abs(df["strike"] - atm)
            closest_strike = int(df.sort_values("diff").iloc[0]["strike"])

            ce = df[(df["strike"] == closest_strike) & (df["option_type"] == "CE")]
            pe = df[(df["strike"] == closest_strike) & (df["option_type"] == "PE")]

            atm = closest_strike

        print("✅ FINAL STRIKE USED:", atm)

        # =========================
        # KEYS (WORKING PART)
        # =========================
        ce_key = ce.iloc[0]["instrument_key"]
        pe_key = pe.iloc[0]["instrument_key"]

        print("CE KEY:", ce_key)
        print("PE KEY:", pe_key)

        # =========================
        # 🔥 STEP 4: QUOTES API (WORKING OI)
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
