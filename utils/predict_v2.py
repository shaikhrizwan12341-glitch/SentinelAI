import os
import joblib
import pandas as pd
from utils.url_features import extract_url_features

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "url_model.pkl")

model = joblib.load(MODEL_PATH)


def predict_url(url: str) -> dict:
    # 1. Extract feature dictionary
    features = extract_url_features(url)

    # 2. Convert to DataFrame with explicit feature names
    X = pd.DataFrame([features])

    if hasattr(model, "feature_names_in_"):
        X = X[model.feature_names_in_]

    # 3. Predict ML class probabilities
    probs = model.predict_proba(X)[0]
    classes = list(model.classes_)

    # Correct Mapping: Class 1 = Phishing | Class 0 = Safe
    phishing_index = classes.index(1) if 1 in classes else 1
    safe_index = classes.index(0) if 0 in classes else 0

    ml_phishing_prob = float(probs[phishing_index])
    ml_safe_prob = float(probs[safe_index])

    # -------------------------------------------------------------
    # 4. Rule-Based Heuristic Overrides (Brand Spoofing)
    # -------------------------------------------------------------
    brand_spoofed = features.get("brand_impersonation", 0) == 1
    has_suspicious_kw = features.get("has_suspicious_keywords", 0) == 1

    if brand_spoofed or (has_suspicious_kw and features.get("hyphen_count", 0) >= 2):
        phishing_prob = max(ml_phishing_prob, 0.95)
        safe_prob = 1.0 - phishing_prob
        override_reason = "Brand impersonation / phishing keywords detected"
    else:
        phishing_prob = ml_phishing_prob
        safe_prob = ml_safe_prob
        override_reason = None

    # 5. Final decision
    if phishing_prob > 0.5:
        prediction = "phishing"
        confidence = phishing_prob
    else:
        prediction = "safe"
        confidence = safe_prob

    result = {
        "url": url,
        "prediction": prediction,
        "confidence": round(float(confidence), 4),
        "phishing_probability": round(float(phishing_prob), 4),
        "safe_probability": round(float(safe_prob), 4),
    }

    if override_reason:
        result["flag"] = override_reason

    return result