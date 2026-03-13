import requests

def get_nifty_price():

    try:

        url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5ENSEI"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            print("API error:", r.status_code)
            return 22450   # fallback price

        data = r.json()

        price = data["quoteResponse"]["result"][0]["regularMarketPrice"]

        return float(price)

    except Exception as e:

        print("PRICE FETCH ERROR:", e)

        # fallback so AI continues running
        return 22450
