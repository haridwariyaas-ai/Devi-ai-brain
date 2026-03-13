def detect_bias(call_oi, put_oi):

    if put_oi > call_oi * 1.2:
        return "Bullish"

    if call_oi > put_oi * 1.2:
        return "Bearish"

    return "Sideways"
