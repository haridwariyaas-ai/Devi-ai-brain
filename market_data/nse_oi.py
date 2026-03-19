import requests

def get_nse_oi(price):

    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)

        res = session.get(url, headers=headers)
        data = res.json()

        records = data["records"]["data"]

        atm = round(price / 50) * 50

        call_oi = 0
        put_oi = 0

        for item in records:

            if item["strikePrice"] == atm:

                if "CE" in item:
                    call_oi = item["CE"]["openInterest"]

                if "PE" in item:
                    put_oi = item["PE"]["openInterest"]

                break

        print("✅ NSE OI:", call_oi, put_oi)

        return {
            "call_oi": call_oi,
            "put_oi": put_oi
        }

    except Exception as e:
        print("❌ NSE ERROR:", e)

    return {"call_oi": 0, "put_oi": 0}
