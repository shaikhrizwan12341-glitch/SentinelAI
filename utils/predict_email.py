from pathlib import Path
import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "email_model.pkl"
VECTORIZER_PATH = PROJECT_ROOT / "models" / "email_vectorizer.pkl"


def load_model():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


def predict_email(email_text: str) -> dict:

    model, vectorizer = load_model()

    features = vectorizer.transform([email_text])

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

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