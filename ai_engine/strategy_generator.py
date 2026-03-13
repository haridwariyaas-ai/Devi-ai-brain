def generate_strategy(bias):

    if bias == "Bullish":

        return "Sell PUT or Bull Put Spread"

    if bias == "Bearish":

        return "Sell CALL or Bear Call Spread"

    return "Iron Condor"
