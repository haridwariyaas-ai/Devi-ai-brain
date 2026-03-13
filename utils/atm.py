def find_atm(price):

    if price is None:
        return None

    return round(price / 50) * 50
