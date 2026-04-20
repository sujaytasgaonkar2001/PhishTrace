from datetime import datetime
import re


SUSPICIOUS_KEYWORDS = [
    "login", "verify", "update", "secure", "account",
    "bank", "paypal", "crypto", "wallet", "signin"
]


def calculate_domain_age_score(creation_date):
    if not creation_date:
        return 20

    try:
        creation = datetime.fromisoformat(creation_date)
        age_days = (datetime.utcnow() - creation).days

        if age_days < 30:
            return 30
        elif age_days < 180:
            return 20
        elif age_days < 365:
            return 10
        else:
            return 0
    except:
        return 20


def keyword_score(domain):
    score = 0
    found = []

    for word in SUSPICIOUS_KEYWORDS:
        if word in domain.lower():
            score += 10
            found.append(word)

    return score, found


def subdomain_score(subdomain):
    if not subdomain:
        return 0

    parts = subdomain.split(".")
    if len(parts) >= 3:
        return 15  # deep nesting → suspicious

    return 5


def dns_score(dns_records):
    score = 0

    if len(dns_records.get("A", [])) > 3:
        score += 10  # fast-flux suspicion

    if dns_records.get("MX") == [""]:
        score += 5

    return score


def calculate_risk(data):
    score = 0
    reasons = []

    # Domain age
    age_score = calculate_domain_age_score(
        data["whois"].get("creation_date")
    )
    score += age_score
    if age_score:
        reasons.append("New or recently registered domain")

    # Keywords
    k_score, words = keyword_score(data["domain"])
    score += k_score
    if words:
        reasons.append(f"Suspicious keywords: {', '.join(words)}")

    # Subdomain abuse
    s_score = subdomain_score(data["subdomain"])
    score += s_score
    if s_score:
        reasons.append("Suspicious subdomain structure")

    # DNS patterns
    d_score = dns_score(data["dns_records"])
    score += d_score
    if d_score:
        reasons.append("Unusual DNS configuration")

    return {
        "score": min(score, 100),
        "risk_level": (
            "low" if score < 30 else
            "medium" if score < 70 else
            "high"
        ),
        "reasons": reasons
    }