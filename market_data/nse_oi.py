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

        # STEP 1 — cookie set
        session.get("https://www.nseindia.com", headers=headers)

        time.sleep(1)

        # STEP 2 — fetch data
        response = session.get(url, headers=headers)

        print("📡 NSE STATUS:", response.status_code)

        data = response.json()

        records = data.get("records", {}).get("data", [])

        print("📊 RECORD COUNT:", len(records))

        if not records:
            return {"call_oi": 0, "put_oi": 0}

        atm = round(price / 50) * 50

        call_oi = 0
        put_oi = 0

        for item in records:

            if item.get("strikePrice") == atm:

                if "CE" in item:
                    call_oi = item["CE"].get("openInterest", 0)

                if "PE" in item:
                    put_oi = item["PE"].get("openInterest", 0)

                break

        print("✅ NSE OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ NSE ERROR:", e)

    return {"call_oi": 0, "put_oi": 0}
