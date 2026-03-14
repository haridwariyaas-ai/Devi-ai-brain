def calculate_pcr(call_oi, put_oi):

    if call_oi == 0:
        return 0

    pcr = put_oi / call_oi

    return round(pcr, 2)
