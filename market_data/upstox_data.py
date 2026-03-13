import requests
import os


def get_nifty_price():

    ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

    if not ACCESS_TOKEN:
        print("Token missing")
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

        r = requests.get(url, headers=headers, params=params)

        data = r.json()

        print("API Response:", data)

        if "data" in data and "NSE_INDEX|Nifty 50" in data["data"]:

            return data["data"]["NSE_INDEX|Nifty 50"]["last_price"]

        else:

            print("Price not found")

            return None

    except Exception as e:

        print("API Error:", e)

        return None            if instrument in data["data"]:

                return data["data"][instrument]["last_price"]

        print("Invalid API response")

        return None

    except Exception as e:

        print("API error:", e)

        return None
