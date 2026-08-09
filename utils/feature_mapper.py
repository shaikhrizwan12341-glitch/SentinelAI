import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

FEATURE_ORDER_PATH = PROJECT_ROOT / "models" / "feature_order.json"


with open(FEATURE_ORDER_PATH, "r") as f:
    FEATURE_ORDER = json.load(f)


def map_features(feature_dict):
    """
    Convert extracted URL features into the exact feature
    order expected by the trained model.
    """

    values = []

    for feature in FEATURE_ORDER:
        if feature not in feature_dict:
            raise KeyError(
                f"Feature '{feature}' is missing from extracted features."
            )

        values.append(feature_dict[feature])

    return values