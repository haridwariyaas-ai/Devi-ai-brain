import pandas as pd
import requests
import os

def get_oi_data(price):
    try:
        token = os.getenv("UPSTOX_ACCESS_TOKEN")
        if not token:
            print("❌ ERROR: No Token")
            return {"strike": 0, "call_oi": 0, "put_oi": 0}

        # 1. ATM Strike Selection (Nifty 50 multiples)
        atm = int(round(float(price) / 50) * 50)
        
        # 2. Load CSV
        csv_path = "data/NSE_FO.csv"
        if not os.path.exists(csv_path):
            print("❌ ERROR: CSV missing")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        df = pd.read_csv(csv_path)
        df.columns = [str(col).lower().strip() for col in df.columns]

        # 3. Filtering for Nifty and Nearest Expiry
        df = df[
            (df["exchange"].str.upper() == "NSE_FO") &
            (df["instrument_type"].str.contains("OPT", na=False)) &
            (df["tradingsymbol"].str.startswith("NIFTY"))
        ].copy()

        df["expiry"] = pd.to_datetime(df["expiry"])
        df = df[df["expiry"] >= pd.Timestamp.today().normalize()]
        nearest_expiry = df["expiry"].min()
        df = df[df["expiry"] == nearest_expiry]

        # 4. Get Instrument Keys
        df["strike"] = df["strike"].astype(float).astype(int)
        strike_df = df[df["strike"] == atm]

        if strike_df.empty:
            print(f"❌ ERROR: Strike {atm} not found")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        # Handle different possible column names for option type
        type_col = 'option_type' if 'option_type' in df.columns else 'instrument_type'
        
        ce_key = strike_df[strike_df["tradingsymbol"].str.endswith("CE")]["instrument_key"].values[0]
        pe_key = strike_df[strike_df["tradingsymbol"].str.endswith("PE")]["instrument_key"].values[0]

        # 5. API Call
        url = "https://api.upstox.com/v2/market-quote/quotes"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}
        params = {"symbol": f"{ce_key},{pe_key}"}
        
        response = requests.get(url, headers=headers, params=params)
        res_json = response.json()

        # --- DEBUG AREA ---
        # If OI is 0, check this print in your terminal:
        # print("DEBUG RESPONSE:", res_json) 
        # ------------------

        if res_json.get("status") != "success":
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        # 6. FIXED DATA EXTRACTION
        data = res_json.get("data", {})
        
        # We must use the instrument_key as the dictionary key
        ce_oi = data.get(ce_key, {}).get("oi", 0)
        pe_oi = data.get(pe_key, {}).get("oi", 0)

        print(f"✅ Strike: {atm} | CE OI: {ce_oi} | PE OI: {pe_oi}")
        
        return {
            "strike": atm,
            "call_oi": ce_oi,
            "put_oi": pe_oi
        }

    except Exception as e:
        print(f"🚨 ERROR: {e}")
        return {"strike": 0, "call_oi": 0, "put_oi": 0}
