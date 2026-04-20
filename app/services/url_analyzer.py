import socket
import tldextract
from urllib.parse import urlparse

from app.services.dns_service import get_dns_records
from app.services.whois_service import get_whois_info
from app.services.risk_engine import calculate_risk

async def analyze_url(url: str):
    parsed = urlparse(url)

    domain_info = tldextract.extract(url)
    domain = f"{domain_info.domain}.{domain_info.suffix}"

    try:
        ip = socket.gethostbyname(domain)
    except Exception:
        ip = None

    dns_data = await get_dns_records(domain)
    whois_data = await get_whois_info(domain)

    risk = calculate_risk({
        "domain": domain,
        "subdomain": domain_info.subdomain,
        "dns_records": dns_data,
        "whois": whois_data
    })

    return {
        "input_url": url,
        "domain": domain,
        "subdomain": domain_info.subdomain,
        "ip_address": ip,
        "scheme": parsed.scheme,
        "dns_records": dns_data,
        "whois": whois_data,
        "risk_analysis": risk   # ✅ NEW
    }