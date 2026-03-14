import random

def detect_candle():

    patterns = [
        "Hammer",
        "Bullish Engulfing",
        "Doji",
        "Bearish Engulfing",
        "None"
    ]

    return random.choice(patterns)
