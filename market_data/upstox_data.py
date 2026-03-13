import requests


def get_nifty_price():

    try:

        url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5ENSEI"

        r = requests.get(url)

        data = r.json()

        print("API RESPONSE:", data)

        price = data["quoteResponse"]["result"][0]["regularMarketPrice"]

        return float(price)

    except Exception as e:

        print("ERROR:", e)

        # fallback price so system doesn't break
        return 22450
