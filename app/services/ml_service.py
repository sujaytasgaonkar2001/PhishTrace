import joblib
import math
import os

MODEL_PATH = os.path.join("ml", "model", "model.pkl")

model = joblib.load(MODEL_PATH)


def entropy(domain):
    prob = [float(domain.count(c)) / len(domain) for c in set(domain)]
    return -sum([p * math.log2(p) for p in prob])


def extract_features(domain):
    return [
        len(domain),
        domain.count("."),
        sum(c.isdigit() for c in domain),
        entropy(domain),
        int("-" in domain),
        int("login" in domain),
        int("secure" in domain),
        int("bank" in domain),
    ]


def predict_domain(domain: str):
    features = [extract_features(domain)]
    prob = model.predict_proba(features)[0][1]
    return float(prob)