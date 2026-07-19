from pathlib import Path

import joblib

from utils.url_features import extract_url_features


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "url_model.pkl"


def load_model():
    """
    Load the trained URL phishing detection model.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def predict_url(url: str) -> dict:
    """
    Predict whether a URL is legitimate or phishing.
    """

    model = load_model()

    features = extract_url_features(url)

    prediction = model.predict([features])[0]

    probabilities = model.predict_proba([features])[0]

    phishing_probability = probabilities[1]

    if prediction == 1:

        return {
            "prediction": "PHISHING",
            "confidence": float(round(phishing_probability * 100, 2)),
            "risk": "High"
        }

    safe_probability = probabilities[0]

    return {
        "prediction": "SAFE",
        "confidence": float(round(safe_probability * 100, 2)),
        "risk": "Low"
    }