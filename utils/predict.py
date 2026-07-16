import random

def predict_url(url):
    """
    Dummy prediction function.
    This will later be replaced by the trained ML model.
    """

    safe = random.choice([True, False])

    if safe:
        return {
            "prediction": "SAFE",
            "confidence": round(random.uniform(95, 99), 2),
            "risk": "Low"
        }

    return {
        "prediction": "PHISHING",
        "confidence": round(random.uniform(90, 99), 2),
        "risk": "High"
    }