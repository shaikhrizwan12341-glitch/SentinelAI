from pathlib import Path

import joblib
import pandas as pd

from utils.url_features import extract_url_features
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "data" / "url_dataset.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "url_model.pkl"


def train_model():
    """
    Train and save the phishing URL detection model.
    """

    print("Loading dataset...")

    data = pd.read_csv(DATASET_PATH)

    print(f"Dataset size: {len(data)}")

    print("Extracting URL features...")

    X = data["url"].apply(extract_url_features).tolist()
    y = data["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("Training Random Forest model...")

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"Model Accuracy: {accuracy * 100:.2f}%")

    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()