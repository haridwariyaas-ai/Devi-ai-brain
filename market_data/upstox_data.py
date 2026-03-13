import requests
import os

def get_nifty_price():

    token = os.getenv("UPSTOX_ACCESS_TOKEN")

    if not token:
        return None

    url = "https://api.upstox.com/v2/market-quote/ltp"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "instrument_key": "NSE_INDEX|Nifty 50"
    }

    r = requests.get(url, headers=headers, params=params)

    data = r.json()

    if "data" in data and "NSE_INDEX|Nifty 50" in data["data"]:
        return data["data"]["NSE_INDEX|Nifty 50"]["last_price"]

    return None
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
