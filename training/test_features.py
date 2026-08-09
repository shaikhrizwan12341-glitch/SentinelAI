from utils.url_features import extract_url_features
from utils.feature_mapper import map_features


# Test URL
url = "https://google.com"

print("=" * 60)
print("Testing Feature Extraction")
print("=" * 60)

# Extract features
features = extract_url_features(url)

print("\nExtracted Features:")
for key, value in features.items():
    print(f"{key}: {value}")

# Map features into model order
mapped = map_features(features)

print("\nMapped Feature Count:", len(mapped))

print("\nMapped Values:")
print(mapped)

print("\nFirst 10 mapped values:")
print(mapped[:10])

print("\n" + "=" * 60)
print("Feature test completed.")
print("=" * 60)