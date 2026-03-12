
def build_trade(direction, atm):

    if direction == "BULLISH":
        return {
            "strategy": "SELL_PE",
            "strike": atm
        }

    elif direction == "BEARISH":
        return {
            "strategy": "SELL_CE",
            "strike": atm
        }

    else:
        return {
            "strategy": "IRON_CONDOR",
            "center": atm
        }
