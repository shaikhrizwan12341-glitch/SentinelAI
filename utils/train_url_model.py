from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from utils.url_features import extract_url_features
from utils.feature_mapper import map_features


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "data" / "url_dataset.csv"
LEGITIMATE_DATASET_PATH = PROJECT_ROOT / "data" / "legitimate_urls.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "url_model.pkl"


# ============================================================
# LOAD ORIGINAL DATASET
# ============================================================

print("=" * 60)
print("Loading datasets...")
print("=" * 60)

df_original = pd.read_csv(DATASET_PATH)

print("Original samples :", len(df_original))

# Keep only URL and label
df_original = df_original[["URL", "label"]]


# ============================================================
# LOAD ADDITIONAL LEGITIMATE URLS
# ============================================================

df_legitimate = pd.read_csv(
    LEGITIMATE_DATASET_PATH
)

print(
    "Additional safe URLs :",
    len(df_legitimate)
)

# Make absolutely sure these URLs are SAFE
df_legitimate["label"] = 1

df_legitimate = df_legitimate[["URL", "label"]]


# ============================================================
# COMBINE DATASETS
# ============================================================

df = pd.concat(
    [
        df_original,
        df_legitimate
    ],
    ignore_index=True
)

print(
    "Combined samples :",
    len(df)
)


# Remove duplicate URLs
df = df.drop_duplicates(
    subset=["URL"]
).reset_index(drop=True)

print(
    "After removing duplicates :",
    len(df)
)


# ============================================================
# VERIFY LABELS
# ============================================================

print("\nLabel distribution:")

print(
    df["label"].value_counts()
    .sort_index()
)

print(
    "\nExpected:"
)

print(
    "0 = PHISHING"
)

print(
    "1 = SAFE"
)


# ============================================================
# EXTRACT FEATURES
# ============================================================

print("\nExtracting URL features...")

feature_dicts = []

total = len(df)

for index, url in enumerate(df["URL"]):

    feature_dict = extract_url_features(url)

    feature_dicts.append(feature_dict)

    if (index + 1) % 10000 == 0:
        print(
            f"Processed {index + 1:,} / {total:,} URLs"
        )


# ============================================================
# MAP FEATURES
# ============================================================

print("\nMapping features...")

X = [
    map_features(feature_dict)
    for feature_dict in feature_dicts
]

y = df["label"]


print(
    "Feature Count :",
    len(X[0])
)

print(
    "Training samples :",
    len(X)
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(
    "\nTraining samples :",
    len(X_train)
)

print(
    "Testing samples  :",
    len(X_test)
)


# ============================================================
# RANDOM FOREST
# ============================================================

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(
    X_train,
    y_train
)


# ============================================================
# EVALUATION
# ============================================================

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\n" + "=" * 60)

print(
    f"Accuracy : {accuracy * 100:.2f}%"
)

print("=" * 60)


print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=[
            "PHISHING",
            "SAFE"
        ],
        zero_division=0
    )
)


print("\nConfusion Matrix\n")

print(
    confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1]
    )
)


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(
    model,
    MODEL_PATH
)

print(
    "\nModel saved successfully!"
)

print(
    "Model path:",
    MODEL_PATH
)