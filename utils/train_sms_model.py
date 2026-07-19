import pandas as pd
import joblib

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

print("Loading dataset...")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("data/sms_dataset.csv")

print(f"Dataset Shape : {df.shape}")

# -----------------------------
# Remove Missing Values
# -----------------------------
df = df.dropna()

print("Missing values removed.")

# -----------------------------
# Features and Labels
# -----------------------------
X = df["text"]
y = df["label"]

# -----------------------------
# Train/Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Train/Test Split Completed")

# -----------------------------
# TF-IDF Vectorizer
# -----------------------------
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

print("TF-IDF Vectorization Completed")

# -----------------------------
# Train Model
# -----------------------------
model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

print("Model Training Completed")

# -----------------------------
# Predictions
# -----------------------------
y_pred = model.predict(X_test)

print("\n========== MODEL PERFORMANCE ==========\n")

print("Accuracy  :", round(accuracy_score(y_test, y_pred), 4))
print("Precision :", round(precision_score(y_test, y_pred), 4))
print("Recall    :", round(recall_score(y_test, y_pred), 4))
print("F1 Score  :", round(f1_score(y_test, y_pred), 4))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report")
print(classification_report(y_test, y_pred))

print("\n=======================================")

# -----------------------------
# Save Model
# -----------------------------
joblib.dump(model, "models/sms_model.pkl")
joblib.dump(vectorizer, "models/sms_vectorizer.pkl")

print("Model Saved Successfully")
print("Model      : models/sms_model.pkl")
print("Vectorizer : models/sms_vectorizer.pkl")
print("=======================================")