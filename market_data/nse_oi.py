print("🔥 NSE OI FILE RUNNING 🔥")

import requests
import time


def get_nse_oi(price):

    try:
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.nseindia.com/",
            "Connection": "keep-alive"
        }

        session = requests.Session()

        # cookie set
        session.get("https://www.nseindia.com", headers=headers)
        time.sleep(1)

        response = session.get(url, headers=headers)

        print("📡 NSE STATUS:", response.status_code)

        if response.status_code != 200:
            print("❌ NSE BLOCKED")
            return {"call_oi": 0, "put_oi": 0}

        data = response.json()

        records = data.get("records", {}).get("data", [])

        print("📊 TOTAL STRIKES:", len(records))

        if not records:
            return {"call_oi": 0, "put_oi": 0}

        # 🔥 STEP — FIND NEAREST STRIKE (IMPORTANT FIX)
        nearest = min(records, key=lambda x: abs(x["strikePrice"] - price))

        strike = nearest["strikePrice"]

        print("🎯 NEAREST STRIKE:", strike)

        call_oi = nearest.get("CE", {}).get("openInterest", 0)
        put_oi = nearest.get("PE", {}).get("openInterest", 0)

        print("✅ FINAL OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ NSE ERROR:", e)

    return {"call_oi": 0, "put_oi": 0}
