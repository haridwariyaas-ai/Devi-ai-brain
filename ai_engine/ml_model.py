import random

def predict_market():

    predictions = [

        {"direction": "Bullish", "confidence": 72},
        {"direction": "Bearish", "confidence": 68},
        {"direction": "Sideways", "confidence": 55}

    ]

    return random.choice(predictions)
