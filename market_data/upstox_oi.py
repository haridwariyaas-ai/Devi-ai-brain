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
        # ✅ STEP 1: ATM (CORRECT)
        # =========================
        atm = int(round(float(price) / 50) * 50)
        print("🎯 IDEAL ATM:", atm)

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
        # 🔥 STEP 2: FUNCTION TO FETCH OI
        # =========================
        def fetch_oi(ce_key, pe_key):
            url = "https://api.upstox.com/v2/market-quote/quotes"

            params = {
                "symbol": f"{ce_key},{pe_key}"
            }

            res = requests.get(url, headers=headers, params=params).json()

            data = res.get("data", {})

            ce_data = None
            pe_data = None

            for k, v in data.items():
                if "CE" in k.upper():
                    ce_data = v
                elif "PE" in k.upper():
                    pe_data = v

            call_oi = ce_data.get("oi", 0) if ce_data else 0
            put_oi = pe_data.get("oi", 0) if pe_data else 0

            return call_oi, put_oi

        # =========================
        # 🔥 STEP 3: TRY EXACT ATM
        # =========================
        ce = df[(df["strike"] == atm) & (df["option_type"] == "CE")]
        pe = df[(df["strike"] == atm) & (df["option_type"] == "PE")]

        if not ce.empty and not pe.empty:
            ce_key = ce.iloc[0]["instrument_key"]
            pe_key = pe.iloc[0]["instrument_key"]

            call_oi, put_oi = fetch_oi(ce_key, pe_key)

            # ✅ अगर OI valid है → return
            if call_oi > 0 or put_oi > 0:
                print("✅ EXACT ATM WORKED")
                return {
                    "strike": atm,
                    "call_oi": call_oi,
                    "put_oi": put_oi
                }

        print("⚠️ EXACT ATM FAILED → TRYING NEAREST")

        # =========================
        # 🔁 STEP 4: FALLBACK TO NEAREST (WORKING LOGIC)
        # =========================
        ce_all = df[df["option_type"] == "CE"].copy()
        pe_all = df[df["option_type"] == "PE"].copy()

        ce_all["diff"] = abs(ce_all["strike"] - atm)
        pe_all["diff"] = abs(pe_all["strike"] - atm)

        atm_ce = ce_all.sort_values("diff").iloc[0]
        atm_pe = pe_all.sort_values("diff").iloc[0]

        strike = int(atm_ce["strike"])

        ce_key = atm_ce["instrument_key"]
        pe_key = atm_pe["instrument_key"]

        call_oi, put_oi = fetch_oi(ce_key, pe_key)

        print("✅ NEAREST STRIKE USED:", strike)

        return {
            "strike": strike,
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("ERROR:", e)
        return {"strike": 0, "call_oi": 0, "put_oi": 0}
