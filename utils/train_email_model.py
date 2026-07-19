import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ----------------------------
# Paths
# ----------------------------

DATA_PATH = "data/email_dataset.csv"

MODEL_DIR = "models"

MODEL_PATH = os.path.join(MODEL_DIR, "email_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "email_vectorizer.pkl")

# ----------------------------
# Load Dataset
# ----------------------------

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset Shape : {df.shape}")

# ----------------------------
# Data Cleaning
# ----------------------------

df = df.dropna()

df["body"] = df["body"].astype(str)

df["label"] = df["label"].astype(int)

print("Missing values removed.")

# ----------------------------
# Features & Labels
# ----------------------------

X = df["body"]

y = df["label"]

# ----------------------------
# Train/Test Split
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Train/Test Split Completed")

# ----------------------------
# TF-IDF Vectorizer
# ----------------------------

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=10000
)

X_train_vector = vectorizer.fit_transform(X_train)

X_test_vector = vectorizer.transform(X_test)

print("TF-IDF Vectorization Completed")

# ----------------------------
# Train Model
# ----------------------------

model = LogisticRegression(max_iter=1000)

model.fit(X_train_vector, y_train)

print("Model Training Completed")

# ----------------------------
# Prediction
# ----------------------------

predictions = model.predict(X_test_vector)

# ----------------------------
# Evaluation
# ----------------------------

print("\n========== MODEL PERFORMANCE ==========\n")

print(f"Accuracy  : {accuracy_score(y_test, predictions):.4f}")
print(f"Precision : {precision_score(y_test, predictions):.4f}")
print(f"Recall    : {recall_score(y_test, predictions):.4f}")
print(f"F1 Score  : {f1_score(y_test, predictions):.4f}")

print("\nConfusion Matrix")

print(confusion_matrix(y_test, predictions))

print("\nClassification Report")

print(classification_report(y_test, predictions))

# ----------------------------
# Save Model
# ----------------------------

os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(model, MODEL_PATH)

joblib.dump(vectorizer, VECTORIZER_PATH)

print("\n=======================================")
print("Model Saved Successfully")
print(f"Model      : {MODEL_PATH}")
print(f"Vectorizer : {VECTORIZER_PATH}")
print("=======================================")