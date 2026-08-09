from pathlib import Path

import joblib
import tldextract

from utils.url_features_v2 import extract_features
from utils.feature_mapper import map_features


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "url_model.pkl"


# ============================================================
# Known legitimate domains
# ============================================================

KNOWN_SAFE_DOMAINS = {
    "google.com",
    "github.com",
    "microsoft.com",
    "apple.com",
    "amazon.com",
    "paypal.com",
    "netflix.com",
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "outlook.com",
}


def normalize_url(url: str) -> str:
    """
    Normalize common URL formatting mistakes.

    Handles:
    - Markdown links
    - Escaped protocols
    - Missing protocols
    """

    url = str(url).strip()

    # Convert Markdown:
    # [https://google.com](https://google.com)
    if url.startswith("[") and "](" in url and url.endswith(")"):
        try:
            url = url.split("](", 1)[1][:-1]
        except Exception:
            pass

    # Remove escaped protocol
    url = url.replace("https\\://", "https://")
    url = url.replace("http\\://", "http://")

    return url


def get_registered_domain(url: str) -> str:
    """
    Extract the registered/root domain.

    Examples:

    www.google.com       -> google.com
    accounts.google.com  -> google.com
    github.com           -> github.com
    attacker.com         -> attacker.com
    """

    normalized = normalize_url(url)

    if not normalized.startswith(("http://", "https://")):
        normalized = "http://" + normalized

    extracted = tldextract.extract(normalized)

    if not extracted.domain or not extracted.suffix:
        return ""

    return f"{extracted.domain}.{extracted.suffix}".lower()


def is_known_safe_domain(url: str) -> bool:
    """
    Check whether the URL belongs to an explicitly trusted
    legitimate domain.

    This uses exact registered-domain matching.
    """

    registered_domain = get_registered_domain(url)

    return registered_domain in KNOWN_SAFE_DOMAINS


def load_model():
    """Load the trained Random Forest model."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def predict_url(url: str):
    """
    Predict whether a URL is SAFE or PHISHING.

    Pipeline:

    1. Normalize URL
    2. Check known legitimate domain
    3. Extract 30 ML features
    4. Map features into training order
    5. Run Random Forest
    6. Add phishing explanation flags
    """

    normalized_url = normalize_url(url)

    # ========================================================
    # STEP 1 — Trusted legitimate domain check
    # ========================================================

    if is_known_safe_domain(normalized_url):

        return {
            "url": normalized_url,
            "prediction": "SAFE",
            "confidence": 1.0,
            "phishing_probability": 0.0,
            "safe_probability": 1.0,
            "flag": "Known legitimate domain",
        }

    # ========================================================
    # STEP 2 — Load model
    # ========================================================

    model = load_model()

    # ========================================================
    # STEP 3 — Extract features
    # ========================================================

    feature_dict = extract_features(normalized_url)

    # ========================================================
    # STEP 4 — Map features
    # ========================================================

    features = map_features(feature_dict)

    # ========================================================
    # STEP 5 — Model prediction
    # ========================================================

    prediction = model.predict([features])[0]

    probabilities = model.predict_proba([features])[0]

    # Model classes:
    # 0 = PHISHING
    # 1 = SAFE

    phishing_probability = float(probabilities[0])
    safe_probability = float(probabilities[1])

    confidence = round(
        max(
            phishing_probability,
            safe_probability
        ),
        4
    )

    # ========================================================
    # STEP 6 — Build result
    # ========================================================

    result = {
        "url": normalized_url,
        "prediction": (
            "SAFE"
            if prediction == 1
            else "PHISHING"
        ),
        "confidence": confidence,
        "phishing_probability": round(
            phishing_probability,
            4
        ),
        "safe_probability": round(
            safe_probability,
            4
        ),
    }

    # ========================================================
    # STEP 7 — Explanation flags
    # ========================================================

    if feature_dict.get(
        "brand_impersonation",
        0
    ) == 1:

        result["flag"] = (
            "Brand impersonation / "
            "phishing keywords detected"
        )

    elif feature_dict.get(
        "has_suspicious_keywords",
        0
    ) == 1:

        result["flag"] = (
            "Suspicious phishing keywords detected"
        )

    return result