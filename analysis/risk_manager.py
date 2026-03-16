def risk_manager(probability, trend):

    if probability >= 70 and trend == "Uptrend":
        return "Low Risk"

    if probability >= 60:
        return "Medium Risk"

    return "High Risk"
