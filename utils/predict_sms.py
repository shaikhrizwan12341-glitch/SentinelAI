import re

PHISHING_KEYWORDS = [
    "otp",
    "bank",
    "account",
    "verify",
    "click",
    "urgent",
    "winner",
    "gift",
    "claim",
    "free",
    "password",
    "login",
    "limited offer",
    "confirm",
    "reward"
]


def predict_sms(sms_text):

    text = sms_text.lower()

    score = 0

    for word in PHISHING_KEYWORDS:
        if re.search(rf"\b{re.escape(word)}\b", text):
            score += 1

    confidence = min(60 + score * 8, 99)

    if score >= 3:
        return {
            "prediction": "PHISHING",
            "confidence": confidence,
            "risk": "High"
        }

    return {
        "prediction": "SAFE",
        "confidence": 100 - confidence,
        "risk": "Low"
    }