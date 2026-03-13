
def build_strategy(atm):

    if atm is None:
        return "No trade"

    return f"Sell Strangle around {atm}"
