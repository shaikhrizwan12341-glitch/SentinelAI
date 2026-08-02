import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FEATURE_ORDER_PATH = PROJECT_ROOT / "models" / "feature_order.json"


with open(FEATURE_ORDER_PATH, "r") as f:
    FEATURE_ORDER = json.load(f)


def map_features(feature_dict):
    """
    Convert extracted features into the exact order
    expected by the trained ML model.

    Missing features are automatically filled with 0.
    """

    values = []

    for feature in FEATURE_ORDER:
        values.append(feature_dict.get(feature, 0))

    return values