from pathlib import Path
import pandas as pd
from tqdm import tqdm

from utils.url_features import extract_url_features

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_DATASET = PROJECT_ROOT / "data" / "url_dataset.csv"
OUTPUT_DATASET = PROJECT_ROOT / "data" / "training_features.csv"

print("Loading dataset...")

df = pd.read_csv(INPUT_DATASET)

print("Dataset Loaded:", len(df))

feature_rows = []

labels = []

print("Extracting features...")

for _, row in tqdm(df.iterrows(), total=len(df)):

    try:

        features = extract_url_features(row["URL"])

        feature_rows.append(features)

        labels.append(row["label"])

    except:

        pass

feature_df = pd.DataFrame(feature_rows)

feature_df["label"] = labels

feature_df.to_csv(OUTPUT_DATASET, index=False)

print()

print("Saved to")

print(OUTPUT_DATASET)

print()

print(feature_df.head())