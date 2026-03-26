import pandas as pd
import requests
import os

print("🔥 upstox_oi.py FINAL loaded")

def get_oi_data(price):
    try:
        print("🚀 OI FUNCTION START")

        token = os.getenv("UPSTOX_ACCESS_TOKEN")

        if not token:
            print("❌ TOKEN MISSING")
            return {"call_oi": 0, "put_oi": 0}

        if price == 0:
            print("❌ PRICE = 0")
            return {"call_oi": 0, "put_oi": 0}

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # =========================
        # LOAD CSV
        # =========================
        df = pd.read_csv("data/NSE_FO.csv")
        print("📊 CSV LOADED:", df.shape)

        # =========================
        # FILTER NIFTY OPTIONS
        # =========================
        df = df[
            (df["exchange"] == "NSE_FO") &
            (df["instrument_type"] == "OPTIDX") &
            (df["tradingsymbol"].str.contains("NIFTY"))
        ].copy()

        print("📊 NIFTY FILTER:", df.shape)

        if df.empty:
            print("❌ NO NIFTY DATA")
            return {"call_oi": 0, "put_oi": 0}

        # =========================
        # EXPIRY FILTER
        # =========================
        df["expiry"] = pd.to_datetime(df["expiry"])
        today = pd.Timestamp.today().normalize()

        df = df[df["expiry"] >= today]

        if df.empty:
            print("❌ NO FUTURE EXPIRY")
            return {"call_oi": 0, "put_oi": 0}

        nearest_expiry = df["expiry"].min()
        df = df[df["expiry"] == nearest_expiry]

        print("📅 EXPIRY:", nearest_expiry)

        # =========================
        # ATM STRIKE
        # =========================
        df["strike_diff"] = abs(df["strike"] - price)
        atm_row = df.sort_values("strike_diff").iloc[0]
        atm_strike = atm_row["strike"]

        print("🎯 ATM:", atm_strike)

        # =========================
        # CE / PE SPLIT
        # =========================
        df["option_type"] = df["tradingsymbol"].str[-2:]

        ce_df = df[df["option_type"] == "CE"].copy()
        pe_df = df[df["option_type"] == "PE"].copy()

        if ce_df.empty or pe_df.empty:
            print("❌ CE/PE NOT FOUND")
            return {"call_oi": 0, "put_oi": 0}

        ce_df["strike_diff"] = abs(ce_df["strike"] - price)
        pe_df["strike_diff"] = abs(pe_df["strike"] - price)

        atm_ce = ce_df.sort_values("strike_diff").iloc[0]
        atm_pe = pe_df.sort_values("strike_diff").iloc[0]

        ce_key = atm_ce["instrument_key"]
        pe_key = atm_pe["instrument_key"]

        print("🟢 CE:", atm_ce["tradingsymbol"])
        print("🔴 PE:", atm_pe["tradingsymbol"])

        print("🎯 KEYS:", ce_key, pe_key)

        # =========================
        # API CALL (IMPORTANT FIX)
        # =========================
        url = "https://api.upstox.com/v2/market-quote/quotes"

        params = {
            "symbol": f"{ce_key},{pe_key}"   # ✅ CORRECT PARAM
        }

        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        print("📡 QUOTES RESPONSE:", data)

        if data.get("status") != "success":
            print("❌ API FAILED")
            return {"call_oi": 0, "put_oi": 0}

        quotes = data.get("data", {})

        if not quotes:
            print("❌ EMPTY QUOTES")
            return {"call_oi": 0, "put_oi": 0}

        # =========================
        # SAFE CE/PE DETECTION
        # =========================
        ce_data = None
        pe_data = None

        for v in quotes.values():
            ts = str(v.get("trading_symbol", "")).upper()

            if "CE" in ts:
                ce_data = v
            elif "PE" in ts:
                pe_data = v

        if ce_data is None or pe_data is None:
            print("❌ CE/PE NOT MATCHED")
            return {"call_oi": 0, "put_oi": 0}

        # =========================
        # FINAL OI
        # =========================
        call_oi = ce_data.get("oi") or 0
        put_oi = pe_data.get("oi") or 0

        print("📊 FINAL OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ ERROR:", e)
        return {"call_oi": 0, "put_oi": 0}
