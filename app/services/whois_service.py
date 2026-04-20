import whois
from datetime import datetime


def normalize_date(date):
    if isinstance(date, list):
        return date[0]
    return date


async def get_whois_info(domain: str):
    try:
        w = whois.whois(domain)

        return {
            "registrar": w.registrar,
            "creation_date": str(normalize_date(w.creation_date)),
            "expiration_date": str(normalize_date(w.expiration_date)),
            "updated_date": str(normalize_date(w.updated_date)),
            "name_servers": w.name_servers
        }
    except Exception:
        return {
            "error": "WHOIS lookup failed"
        }