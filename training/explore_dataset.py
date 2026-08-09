import pandas as pd

df = pd.read_csv("data/url_dataset.csv")

print("\nColumns in Dataset:\n")
print(df.columns.tolist())