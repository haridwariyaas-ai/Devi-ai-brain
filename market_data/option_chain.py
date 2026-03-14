import random

def get_option_chain():

    # temporary demo data
    call_oi = random.randint(100000, 200000)
    put_oi = random.randint(100000, 200000)

    return {

        "call_oi": call_oi,
        "put_oi": put_oi

    }
