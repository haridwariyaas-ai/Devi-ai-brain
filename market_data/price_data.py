import requests

def get_nifty_price():

    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5ENSEI"

    r = requests.get(url)

    data = r.json()

    price = data["quoteResponse"]["result"][0]["regularMarketPrice"]

    return price
