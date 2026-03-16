def trade_score(probability, ml_confidence, trend, volume_strength):

    score = 0

    score += probability
    score += ml_confidence

    if trend == "Uptrend":
        score += 10

    if volume_strength == "High Volume":
        score += 10

    return min(score, 100)
