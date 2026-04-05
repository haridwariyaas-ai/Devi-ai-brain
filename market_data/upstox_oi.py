import pandas as pd
import requests
import os

def get_oi_data(price):
    try:
        # 1. Token Check
        token = os.getenv("UPSTOX_ACCESS_TOKEN")
        if not token:
            print("❌ ERROR: UPSTOX_ACCESS_TOKEN not found in Environment Variables")
            return {"strike": 0, "call_oi": 0, "put_oi": 0}
        
        if price <= 0:
            print("❌ ERROR: Input price is 0 or negative")
            return {"strike": 0, "call_oi": 0, "put_oi": 0}

        # 2. Strike Selection Logic
        # Nifty moves in 50 point intervals. 
        atm = int(round(float(price) / 50) * 50)
        
        # 3. Load CSV with Error Handling
        csv_path = "data/NSE_FO.csv"
        if not os.path.exists(csv_path):
            print(f"❌ ERROR: File not found at {csv_path}")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        df = pd.read_csv(csv_path)

        # 4. Standardizing Column Names (Fixes "Strike 0" issue)
        # Force columns to lowercase to avoid "Strike" vs "strike" errors
        df.columns = [str(col).lower().strip() for col in df.columns]

        # 5. Filtering Logic
        # We look for NIFTY (not FINNIFTY) and the nearest expiry
        mask = (
            (df["exchange"].str.upper() == "NSE_FO") &
            (df["instrument_type"].str.contains("OPT", na=False)) &
            (df["tradingsymbol"].str.startswith("NIFTY"))
        )
        df = df[mask].copy()

        if df.empty:
            print("❌ ERROR: No NIFTY options found in CSV after filtering")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        # Convert expiry and find nearest
        df["expiry"] = pd.to_datetime(df["expiry"])
        today = pd.Timestamp.now().normalize()
        df = df[df["expiry"] >= today]
        
        nearest_expiry = df["expiry"].min()
        df = df[df["expiry"] == nearest_expiry]

        # 6. Find Instrument Keys
        df["strike"] = df["strike"].astype(float).astype(int)
        strike_df = df[df["strike"] == atm]

        if strike_df.empty:
            print(f"❌ ERROR: Strike {atm} not found for expiry {nearest_expiry.date()}")
            # Try to find the closest available strike in the CSV if exact ATM fails
            available_strikes = df["strike"].unique()
            print(f"Available strikes nearby: {sorted(available_strikes)[:10]}")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        # Get Keys
        try:
            # We use 'option_type' or 'instrument_type' depending on your CSV header
            # Using 'tradingsymbol' suffix as a fallback
            ce_key = strike_df[strike_df["tradingsymbol"].str.endswith("CE")]["instrument_key"].values[0]
            pe_key = strike_df[strike_df["tradingsymbol"].str.endswith("PE")]["instrument_key"].values[0]
        except Exception as e:
            print(f"❌ ERROR identifying CE/PE keys: {e}")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        # 7. API Call for OI
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
        url = "https://api.upstox.com/v2/market-quote/quotes"
        params = {"symbol": f"{ce_key},{pe_key}"}
        
        response = requests.get(url, headers=headers, params=params)
        res_json = response.json()

        if res_json.get("status") != "success":
            print(f"❌ API ERROR: {res_json.get('errors')}")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        # 8. Extract Data
        data = res_json.get("data", {})
        ce_oi = data.get(ce_key, {}).get("oi", 0)
        pe_oi = data.get(pe_key, {}).get("oi", 0)

        print(f"✅ SUCCESS: ATM {atm} | CE_OI: {ce_oi} | PE_OI: {pe_oi}")
        
        return {
            "strike": atm,
            "call_oi": ce_oi,
            "put_oi": pe_oi
        }

    except Exception as e:
        print(f"🚨 CRITICAL SYSTEM ERROR: {e}")
        return {"strike": 0, "call_oi": 0, "put_oi": 0}
