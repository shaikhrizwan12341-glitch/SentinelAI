from urllib.parse import urlparse


def explain_url(url, result):
    """Generate explanation for URL scan."""

    reasons = []

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # HTTPS
    if url.startswith("https://"):
        reasons.append("Uses secure HTTPS protocol.")
    else:
        reasons.append("Uses insecure HTTP protocol.")

    # URL Length
    if len(url) > 75:
        reasons.append("URL is unusually long.")
    else:
        reasons.append("URL length appears normal.")

    # Suspicious Keywords
    keywords = [
        "login",
        "verify",
        "secure",
        "update",
        "bank",
        "paypal",
        "gift",
        "reward",
        "claim",
        "free"
    ]

    found = [word for word in keywords if word in url.lower()]

    if found:
        reasons.append(
            "Suspicious keywords detected: " + ", ".join(found)
        )
    else:
        reasons.append("No suspicious keywords detected.")

    # Subdomains
    if domain.count(".") >= 3:
        reasons.append("Multiple subdomains detected.")
    else:
        reasons.append("Domain structure appears normal.")

    if result["prediction"] == "SAFE":
        summary = "The AI model found no major phishing indicators."
    else:
        summary = "The AI model detected multiple phishing indicators."

    return summary, reasons


def explain_email(email_text, result):
    """Generate explanation for email scan."""

    text = email_text.lower()

    reasons = []

    keywords = [
        "verify",
        "account",
        "bank",
        "password",
        "login",
        "urgent",
        "click",
        "reward",
        "winner",
        "gift",
        "otp",
        "security"
    ]

    detected = [
        word for word in keywords
        if word in text
    ]

    if detected:
        reasons.append(
            "Suspicious keywords detected: " + ", ".join(detected)
        )
    else:
        reasons.append("No suspicious keywords detected.")

    if "http://" in text or "https://" in text:
        reasons.append("Contains clickable links.")
    else:
        reasons.append("No external links detected.")

    if "!" in email_text:
        reasons.append("Urgent language detected.")
    else:
        reasons.append("Language appears normal.")

    if result["prediction"] == "SAFE":
        summary = "The AI model found no major phishing indicators."
    else:
        summary = "The AI model detected multiple phishing indicators."

    return summary, reasons
def explain_sms(sms_text, result):
    """
    Generate AI explanation for SMS scans.
    """

    text = sms_text.lower()
    reasons = []

    phishing_keywords = [
        "bank",
        "account",
        "otp",
        "verify",
        "login",
        "password",
        "click",
        "claim",
        "winner",
        "reward",
        "gift",
        "urgent",
        "confirm",
        "limited",
        "offer",
        "free"
    ]

    detected = [
        word for word in phishing_keywords
        if word in text
    ]

    if detected:
        reasons.append(
            f"⚠️ Suspicious keywords detected: {', '.join(detected)}"
        )
    else:
        reasons.append("✅ No suspicious phishing keywords detected.")

    if "http://" in text or "https://" in text:
        reasons.append("⚠️ SMS contains a clickable link.")
    else:
        reasons.append("✅ No external links detected.")

    if "!" in sms_text:
        reasons.append("⚠️ Urgent language detected.")
    else:
        reasons.append("✅ Language appears normal.")

    if result["confidence"] >= 90:
        reasons.append(
            f"🤖 Model confidence is very high ({result['confidence']}%)."
        )
    else:
        reasons.append(
            f"🤖 Model confidence is moderate ({result['confidence']}%)."
        )

    if result["prediction"] == "SAFE":
        summary = (
            "The AI model found no significant phishing indicators in this SMS."
        )
    else:
        summary = (
            "The AI model detected multiple phishing characteristics in this SMS."
        )

    return summary, reasons