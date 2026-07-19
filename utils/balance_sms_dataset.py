import pandas as pd

# Load dataset
df = pd.read_csv("data/SMSSpamCollection.csv", header=None, names=["raw"])

# Split the single column into label and text
df[["label", "text"]] = df["raw"].str.split("\t", n=1, expand=True)

# Keep only required columns
df = df[["text", "label"]]

# Convert labels to numeric
df["label"] = df["label"].map({
    "ham": 0,
    "spam": 1
})

# Separate classes
spam = df[df["label"] == 1]
ham = df[df["label"] == 0]

# Downsample ham to match spam
ham = ham.sample(
    n=len(spam),
    random_state=42
)

# Combine and shuffle
balanced = pd.concat([spam, ham])

balanced = balanced.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# Save balanced dataset
balanced.to_csv(
    "data/sms_dataset.csv",
    index=False
)

print("Balanced Dataset Created")
print(balanced["label"].value_counts())