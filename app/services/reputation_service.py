TOP_DOMAINS = set()


def load_tranco(file_path="ml/data/tranco.csv", limit=100000):
    global TOP_DOMAINS

    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            if i >= limit:
                break

            parts = line.strip().split(",")
            if len(parts) >= 2:
                domain = parts[1]
                TOP_DOMAINS.add(domain.lower())


def is_legit_domain(domain: str):
    return domain.lower() in TOP_DOMAINS