import random

def get_live_option_chain():

    strikes = [22400, 22450, 22500, 22550]

    data = []

    for strike in strikes:

        data.append({

            "strike": strike,
            "call_oi": random.randint(50000, 150000),
            "put_oi": random.randint(50000, 150000)

        })

    return data
