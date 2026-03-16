import random

def get_upstox_live_chain():

    strikes = [22400, 22450, 22500, 22550]

    data = []

    for strike in strikes:

        data.append({

            "strike": strike,
            "call_oi": random.randint(50000, 200000),
            "put_oi": random.randint(50000, 200000)

        })

    return data
