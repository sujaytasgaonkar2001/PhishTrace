import dns.resolver


async def get_dns_records(domain: str):
    resolver = dns.resolver.Resolver()

    records = {
        "A": [],
        "AAAA": [],
        "NS": [],
        "MX": []
    }

    try:
        answers = resolver.resolve(domain, "A")
        records["A"] = [r.to_text() for r in answers]
    except:
        pass

    try:
        answers = resolver.resolve(domain, "AAAA")
        records["AAAA"] = [r.to_text() for r in answers]
    except:
        pass

    try:
        answers = resolver.resolve(domain, "NS")
        records["NS"] = [r.to_text() for r in answers]
    except:
        pass

    try:
        answers = resolver.resolve(domain, "MX")
        records["MX"] = [r.exchange.to_text() for r in answers]
    except:
        pass

    return records