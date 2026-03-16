import random

def analyze_volume():

    volume = random.randint(100000, 500000)

    if volume > 300000:
        strength = "High Volume"

    else:
        strength = "Normal Volume"

    return volume, strength
