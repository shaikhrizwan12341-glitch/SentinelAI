import re

PHISHING_KEYWORDS = [
    "verify",
    "login",
    "bank",
    "account",
    "password",
    "click",
    "urgent",
    "winner",
    "free",
    "gift",
    "claim",
    "otp",
    "suspended",
    "confirm",
    "limited time"
]


def predict_email(email_text):

    text = email_text.lower()

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