def find_atm(price):

    if price is None:
        return "Price not available"

    return round(price / 50) * 50
