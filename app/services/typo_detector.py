import Levenshtein

POPULAR_BRANDS = [
    "facebook", "google", "paypal", "amazon", "microsoft",
    "apple", "netflix", "instagram", "bankofamerica"
]


def detect_typosquat(domain: str):
    domain_name = domain.split(".")[0]

    matches = []

    for brand in POPULAR_BRANDS:
        distance = Levenshtein.distance(domain_name, brand)

        # close match but not exact
        if 1 <= distance <= 2:
            matches.append({
                "brand": brand,
                "distance": distance
            })

    return matches