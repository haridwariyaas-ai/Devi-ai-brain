import pandas as pd
import requests
import os
import io
from datetime import datetime

def update_instrument_csv():
    """Downloads the latest NSE_FO instrument file from Upstox."""
    url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
    csv_path = "data/NSE_FO.csv"
    
    # Create directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    print("Checking for instrument updates...")
    
    # Update only if file doesn't exist or is older than 24 hours
    if os.path.exists(csv_path):
        file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(csv_path))
        if file_age.days < 1:
            print("✅ CSV is up to date.")
            return

    try:
        print("📥 Downloading latest instruments (this may take a moment)...")
        response = requests.get(url)
        if response.status_code == 200:
            # Upstox provides a gzipped CSV; pandas handles decompression automatically
            df_all = pd.read_csv(io.BytesIO(response.content), compression='gzip')
            
            # Filter only for NSE Futures & Options to keep the file small
            df_fo = df_all[df_all['exchange'] == 'NSE_FO']
            df_fo.to_csv(csv_path, index=False)
            print(f"✅ Successfully updated {csv_path}")
        else:
            print("❌ Failed to download CSV from Upstox.")
    except Exception as e:
        print(f"🚨 Error updating CSV: {e}")

def get_oi_data(price):
    try:
        # 1. Update CSV first
        update_instrument_csv()
        
        token = os.getenv("UPSTOX_ACCESS_TOKEN")
        if not token:
            print("❌ ERROR: Missing UPSTOX_ACCESS_TOKEN")
            return {"strike": 0, "call_oi": 0, "put_oi": 0}

        # 2. Strike Selection (ATM)
        atm = int(round(float(price) / 50) * 50)

        # 3. Load and Filter
        df = pd.read_csv("data/NSE_FO.csv")
        df.columns = [str(col).lower().strip() for col in df.columns]

        # Filter for NIFTY Options
        df = df[
            (df["exchange"] == "nse_fo") & 
            (df["instrument_type"] == "OPTIDX") & 
            (df["tradingsymbol"].str.startswith("NIFTY"))
        ].copy()

        # Get Nearest Expiry
        df["expiry"] = pd.to_datetime(df["expiry"])
        today = pd.Timestamp.now().normalize()
        df = df[df["expiry"] >= today]
        nearest_expiry = df["expiry"].min()
        df = df[df["expiry"] == nearest_expiry]

        # 4. Find Instrument Keys
        df["strike"] = df["strike"].astype(float).astype(int)
        strike_df = df[df["strike"] == atm]

        if strike_df.empty:
            print(f"❌ Strike {atm} not found in current expiry.")
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        # Identify CE and PE keys
        ce_key = strike_df[strike_df["tradingsymbol"].str.endswith("CE")]["instrument_key"].values[0]
        pe_key = strike_df[strike_df["tradingsymbol"].str.endswith("PE")]["instrument_key"].values[0]

        # 5. API Call for Live OI
        url = "https://api.upstox.com/v2/market-quote/quotes"
        headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}
        params = {"symbol": f"{ce_key},{pe_key}"}
        
        res = requests.get(url, headers=headers, params=params).json()

        if res.get("status") != "success":
            print("📡 API Error:", res.get("errors"))
            return {"strike": atm, "call_oi": 0, "put_oi": 0}

        # 6. Extracting OI (Final Check)
        data = res.get("data", {})
        
        # Access by the specific instrument key string
        ce_oi = data.get(ce_key, {}).get("oi", 0)
        pe_oi = data.get(pe_key, {}).get("oi", 0)

        print(f"🚀 SUCCESS | Strike: {atm} | CE OI: {ce_oi} | PE OI: {pe_oi}")
        
        return {
            "strike": atm,
            "call_oi": ce_oi,
            "put_oi": pe_oi
        }

    except Exception as e:
        print(f"🚨 CRITICAL ERROR: {e}")
        return {"strike": 0, "call_oi": 0, "put_oi": 0}

# Example:
# print(get_oi_data(22534.20))
