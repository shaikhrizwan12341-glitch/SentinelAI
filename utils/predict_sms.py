from pathlib import Path
import joblib

# -----------------------------
# Project Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "sms_model.pkl"
VECTORIZER_PATH = PROJECT_ROOT / "models" / "sms_vectorizer.pkl"


# -----------------------------
# Load Model
# -----------------------------
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    if not VECTORIZER_PATH.exists():
        raise FileNotFoundError(f"Vectorizer not found: {VECTORIZER_PATH}")

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    return model, vectorizer


# -----------------------------
# Predict SMS
# -----------------------------
def predict_sms(sms_text: str):

    model, vectorizer = load_model()

    sms_vector = vectorizer.transform([sms_text])

    prediction = model.predict(sms_vector)[0]

    probabilities = model.predict_proba(sms_vector)[0]

    phishing_probability = probabilities[1]

    if prediction == 1:
        return {
            "prediction": "PHISHING",
            "confidence": round(phishing_probability * 100, 2),
            "risk": "High"
        }

    safe_probability = probabilities[0]

    return {
        "prediction": "SAFE",
        "confidence": round(safe_probability * 100, 2),
        "risk": "Low"
    }