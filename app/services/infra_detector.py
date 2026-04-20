def detect_ns_impersonation(domain, ns_records):
    domain_name = domain.split(".")[0]

    suspicious = []

    for ns in ns_records:
        ns_lower = ns.lower()

        if domain_name not in ns_lower:
            # If nameserver belongs to big brand
            if "facebook" in ns_lower:
                suspicious.append("facebook")

    return suspicious