from pathlib import Path

import joblib
import numpy as np

from utils.feature_mapper import map_features
from utils.legitimate_domains import (
    get_brand_impersonation_flag,
    is_trusted_domain,
)
from utils.url_features import extract_url_features


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "url_model.pkl"


def load_model():
    """
    Load the trained URL classification model.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"URL model not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def predict_url(url: str) -> dict:
    """
    Predict whether a URL is SAFE or PHISHING.

    Detection pipeline:

        URL
        ↓
        Trusted-domain check
        ↓
        Brand impersonation check
        ↓
        Feature extraction
        ↓
        Feature mapping
        ↓
        ML model
        ↓
        Prediction + confidence + flag
    """

    if not isinstance(url, str):
        raise TypeError("URL must be a string.")

    url = url.strip()

    if not url:
        raise ValueError("URL cannot be empty.")

    # ---------------------------------------------------------
    # Layer 1: Trusted legitimate-domain protection
    # ---------------------------------------------------------

    if is_trusted_domain(url):
        return {
            "prediction": "SAFE",
            "confidence": 1.0,
            "probabilities": {
                "phishing": 0.0,
                "safe": 1.0,
            },
            "flag": "Known legitimate domain",
        }

    # ---------------------------------------------------------
    # Layer 2: Brand impersonation detection
    # ---------------------------------------------------------

    brand_flag = get_brand_impersonation_flag(url)

    if brand_flag:
        return {
            "prediction": "PHISHING",
            "confidence": 1.0,
            "probabilities": {
                "phishing": 1.0,
                "safe": 0.0,
            },
            "flag": brand_flag,
        }

    # ---------------------------------------------------------
    # Layer 3: Machine-learning URL classification
    # ---------------------------------------------------------

    model = load_model()

    # Extract the same 30 features used during model training.
    features = extract_url_features(url)

    # Map features into the trained model's expected order.
    mapped_features = map_features(features)

    # map_features() returns a Python list.
    # Convert it to NumPy and reshape it into one sample.
    mapped_features = np.asarray(
        mapped_features,
        dtype=float,
    ).reshape(1, -1)

    # Predict class.
    prediction = model.predict(mapped_features)[0]

    # Get class probabilities.
    probabilities = model.predict_proba(mapped_features)[0]

    # Model convention:
    # class 0 = PHISHING
    # class 1 = SAFE

    phishing_probability = float(probabilities[0])
    safe_probability = float(probabilities[1])

    # ---------------------------------------------------------
    # Final classification
    # ---------------------------------------------------------

    if prediction == 0:
        final_prediction = "PHISHING"
        confidence = phishing_probability

        flag = None

        if phishing_probability >= 0.80:
            flag = "High-confidence phishing detection"
        elif phishing_probability >= 0.60:
            flag = "Potentially suspicious URL"

    else:
        final_prediction = "SAFE"
        confidence = safe_probability
        flag = None

    return {
        "prediction": final_prediction,
        "confidence": float(round(confidence, 4)),
        "probabilities": {
            "phishing": float(round(phishing_probability, 4)),
            "safe": float(round(safe_probability, 4)),
        },
        "flag": flag,
    }