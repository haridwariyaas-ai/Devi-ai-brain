def oi_heatmap(option_chain):

    max_call = max(option_chain, key=lambda x: x["call_oi"])
    max_put = max(option_chain, key=lambda x: x["put_oi"])

    resistance = max_call["strike"]
    support = max_put["strike"]

    return support, resistance
