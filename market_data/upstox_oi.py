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

        # 🔥 ATM
        atm = int(round(price / 50) * 50)

        print("🎯 ATM:", atm)

        # 🔥 MANUAL SYMBOL BUILD (WORKING FORMAT)
        # Example: NIFTY 23300 CE
        ce_symbol = f"NSE_FO|NIFTY{atm}CE"
        pe_symbol = f"NSE_FO|NIFTY{atm}PE"

        print("CE SYMBOL:", ce_symbol)
        print("PE SYMBOL:", pe_symbol)

        url = "https://api.upstox.com/v2/market-quote/quotes"

        params = {
            "symbol": f"{ce_symbol},{pe_symbol}"
        }

        res = requests.get(url, headers=headers, params=params).json()

        print("📡 RESPONSE:", res)

        data = res.get("data", {})

        ce_data = None
        pe_data = None

        for k, v in data.items():
            if "CE" in k.upper():
                ce_data = v
            elif "PE" in k.upper():
                pe_data = v

        return {
            "strike": atm,
            "call_oi": ce_data.get("oi", 0) if ce_data else 0,
            "put_oi": pe_data.get("oi", 0) if pe_data else 0
        }

    except Exception as e:
        print("ERROR:", e)
        return {"strike": 0, "call_oi": 0, "put_oi": 0}
