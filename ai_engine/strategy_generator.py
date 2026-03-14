def generate_strategy(bias, pcr):

    if bias == "Bullish":

        if pcr > 1.2:
            return "Sell PUT"

        return "Bull Put Spread"

    if bias == "Bearish":

        if pcr < 0.8:
            return "Sell CALL"

        return "Bear Call Spread"

    return "Iron Condor"
