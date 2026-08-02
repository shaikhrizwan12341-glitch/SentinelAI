from utils.url_features_v2 import extract_features
from utils.feature_mapper import map_features

url = "https://google.com"

features = extract_features(url)

print("Extracted Features:")
print(features)

mapped = map_features(features)

print("\nMapped Feature Count:", len(mapped))

print("\nFirst 10 mapped values:")
print(mapped[:10])