
def make_decision(option_chain):

    pcr = option_chain.get("PCR",1)

    if pcr > 1.1:
        return "BULLISH"

    elif pcr < 0.9:
        return "BEARISH"

    else:
        return "SIDEWAYS"
