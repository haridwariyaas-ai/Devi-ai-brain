def final_decision(strategy, probability, risk):

    if probability >= 70 and risk == "Low Risk":
        return f"Execute Trade: {strategy}"

    if probability >= 60:
        return f"Watch Trade: {strategy}"

    return "No Trade"
