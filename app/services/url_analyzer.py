import socket
import tldextract
from urllib.parse import urlparse

from app.services.dns_service import get_dns_records
from app.services.whois_service import get_whois_info
from app.services.risk_engine import calculate_risk
from app.services.ml_service import predict_domain
from app.services.typo_detector import detect_typosquat
from app.services.reputation_service import is_legit_domain


async def analyze_url(url: str):
    # --- Parse URL ---
    parsed = urlparse(url)

    domain_info = tldextract.extract(url)
    domain = f"{domain_info.domain}.{domain_info.suffix}"

    # --- Typosquat detection (NOW correct position) ---
    typo_matches = detect_typosquat(domain)

    # --- Resolve IP ---
    try:
        ip = socket.gethostbyname(domain)
    except Exception:
        ip = None

    # --- Fetch external data ---
    dns_data = await get_dns_records(domain)
    whois_data = await get_whois_info(domain)

    # --- ML prediction (ONLY once) ---
    ml_prob = predict_domain(domain)

    # --- Reputation check ---
    is_legit = is_legit_domain(domain)

    # --- Base risk ---
    risk = calculate_risk({
        "domain": domain,
        "subdomain": domain_info.subdomain,
        "dns_records": dns_data,
        "whois": whois_data,
        "ip_address": ip
    })

    # --- ML ---
    risk["ml_score"] = round(ml_prob * 100, 2)

    # --- TRANC0 (Whitelist) ---
    if is_legit:
        risk["score"] -= 40
        risk["reasons"].append("Top-ranked legitimate domain")

    # --- TYPO DETECTION ---
    if typo_matches and not is_legit:
        risk["score"] += 60
        risk["reasons"].append(
            f"Possible typosquatting of: {', '.join([m['brand'] for m in typo_matches])}"
        )

    # --- ML BOOST ---
    risk["score"] += int(ml_prob * 40)

    # --- Clamp + final level ---
    risk["score"] = max(0, min(100, risk["score"]))
    risk["risk_level"] = (
        "low" if risk["score"] < 40 else
        "medium" if risk["score"] < 70 else
        "high"
    )

    return {
        "input_url": url,
        "domain": domain,
        "subdomain": domain_info.subdomain,
        "ip_address": ip,
        "scheme": parsed.scheme,
        "dns_records": dns_data,
        "whois": whois_data,
        "risk_analysis": risk
    }