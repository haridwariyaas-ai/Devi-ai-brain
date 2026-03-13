import requests
import os


def get_nifty_price():

    ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

    if ACCESS_TOKEN is None:
        print("Access token not set")
        return None

    url = "https://api.upstox.com/v2/market-quote/ltp"

    params = {
        "instrument_key": "NSE_INDEX|Nifty 50"
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json"
    }

    try:

        response = requests.get(url, headers=headers, params=params)

        data = response.json()

        # debugging print
        print("API Response:", data)

        if "data" in data:

            instrument = "NSE_INDEX|Nifty 50"

            if instrument in data["data"]:

                return data["data"][instrument]["last_price"]

        print("Invalid API response")

        return None

    except Exception as e:

        print("API error:", e)

        return None
