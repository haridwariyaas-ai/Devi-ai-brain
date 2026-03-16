def classify_signal(score):

    if score >= 80:
        return "STRONG TRADE"

    if score >= 65:
        return "TRADE"

    if score >= 50:
        return "WATCH"

    return "AVOID"
