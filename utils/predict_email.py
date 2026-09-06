from pathlib import Path
import joblib
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "email_model.pkl"
VECTORIZER_PATH = PROJECT_ROOT / "models" / "email_vectorizer.pkl"


def load_model():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


def to_python_type(value):
    """
    Convert NumPy scalars (np.float64, np.int32, np.bool_) into native Python types.
    Leaves normal Python types untouched.
    """
    if isinstance(value, np.generic):
        return value.item()
    return value


def predict_email(email_text: str) -> dict:
    model, vectorizer = load_model()
    features = vectorizer.transform([email_text])

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    # Cast to Python float first
    phishing_probability = float(probabilities[1])
    safe_probability = float(probabilities[0])

    if prediction == 1:
        return {
            "prediction": "PHISHING",
            "confidence": to_python_type(round(phishing_probability, 4)),
            "risk": "High"
        }

    return {
        "prediction": "SAFE",
        "confidence": to_python_type(round(safe_probability, 4)),
        "risk": "Low"
        }
