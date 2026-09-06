from pathlib import Path
import joblib
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "sms_model.pkl"
VECTORIZER_PATH = PROJECT_ROOT / "models" / "sms_vectorizer.pkl"


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    if not VECTORIZER_PATH.exists():
        raise FileNotFoundError(f"Vectorizer not found: {VECTORIZER_PATH}")

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


def predict_sms(sms_text: str) -> dict:
    model, vectorizer = load_model()
    sms_vector = vectorizer.transform([sms_text])

    prediction = model.predict(sms_vector)[0]
    probabilities = model.predict_proba(sms_vector)[0]

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
