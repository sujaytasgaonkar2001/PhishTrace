import pandas as pd

# Load phishing dataset (PhishTank)
phish_df = pd.read_csv("ml/data/phishtank.csv")

# Extract domain from URL
phish_df["domain"] = phish_df["url"].str.extract(r"https?://([^/]+)")
phish_df["label"] = 1

phish_df = phish_df[["domain", "label"]]

# Load legit dataset (Tranco)
legit_df = pd.read_csv("ml/data/tranco.csv", header=None)
legit_df.columns = ["rank", "domain"]
legit_df["label"] = 0

legit_df = legit_df[["domain", "label"]]

# Combine
df = pd.concat([phish_df, legit_df])

# Clean
df = df.dropna()
df = df.drop_duplicates()

# Save
df.to_csv("ml/data/domains.csv", index=False)

print("Dataset prepared:", df.shape)