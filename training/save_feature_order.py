from pathlib import Path
import json
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET = PROJECT_ROOT / "data" / "url_dataset.csv"

df = pd.read_csv(DATASET)

features = list(df.drop(columns=["FILENAME", "URL", "label"]).columns)

output = PROJECT_ROOT / "models" / "feature_order.json"

with open(output, "w") as f:
    json.dump(features, f, indent=4)

print("Saved", len(features), "features.")
print("File:", output)