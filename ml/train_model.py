import pandas as pd
import math
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def entropy(domain):
    prob = [float(domain.count(c)) / len(domain) for c in set(domain)]
    return -sum([p * math.log2(p) for p in prob])


def extract_features(domain):
    return {
        "length": len(domain),
        "dots": domain.count("."),
        "digits": sum(c.isdigit() for c in domain),
        "entropy": entropy(domain),
        "has_hyphen": int("-" in domain),
        "has_login": int("login" in domain),
        "has_secure": int("secure" in domain),
        "has_bank": int("bank" in domain),
    }


# Load dataset
df = pd.read_csv("ml/data/domains.csv")

# Features
X = df["domain"].apply(extract_features).apply(pd.Series)
y = df["label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "ml/model/model.pkl")

print("Model trained successfully")
print("Accuracy:", model.score(X_test, y_test))