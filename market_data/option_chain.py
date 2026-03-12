
import random

def get_option_chain():

    return {
        "PCR": round(random.uniform(0.7,1.3),2),
        "CE_OI": random.randint(100000,500000),
        "PE_OI": random.randint(100000,500000)
    }
