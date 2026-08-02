from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "data" / "training_features.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "url_model.pkl"

print("Loading extracted feature dataset...")

df = pd.read_csv(DATASET_PATH)

X = df.drop(columns=["label"])
print(list(X.columns))

y = df["label"]

print(f"Training Samples : {len(df)}")
print(f"Feature Count    : {X.shape[1]}")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print("\nTraining Random Forest...\n")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=20,
    min_samples_split=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("=" * 60)
print(f"Accuracy : {accuracy*100:.2f}%")
print("=" * 60)

print("\nClassification Report\n")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix\n")
print(confusion_matrix(y_test, predictions))

joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully!")
print(MODEL_PATH)