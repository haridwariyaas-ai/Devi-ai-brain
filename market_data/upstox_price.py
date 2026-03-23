import requests
import os


def get_price():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    if not token:
        return 0

    url = "https://api.upstox.com/v2/market-quote/ltp"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "instrument_key": "NSE_INDEX|Nifty 50"
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        data = r.json()

        if "data" not in data:
            return 0

        return list(data["data"].values())[0]["last_price"]

    except:
        return 0
