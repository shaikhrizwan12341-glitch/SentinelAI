import ipaddress
import math
import re
from collections import Counter
from urllib.parse import urlparse
import tldextract


# Target brands frequently impersonated in phishing attacks
TARGET_BRANDS = [
    "paypal", "google", "apple", "microsoft", "amazon", "netflix",
    "facebook", "instagram", "chase", "wellsfargo", "bankofamerica",
    "binance", "coinbase", "steam", "linkedin", "twitter", "outlook"
]


def has_ip_address(hostname: str) -> int:
    try:
        ipaddress.ip_address(hostname)
        return 1
    except ValueError:
        return 0


def calculate_entropy(text: str) -> float:
    if not text:
        return 0
    counts = Counter(text)
    length = len(text)
    entropy = 0
    for value in counts.values():
        probability = value / length
        entropy -= probability * math.log2(probability)
    return round(entropy, 4)


def extract_url_features(url: str) -> dict:
    """
    Extract numerical features from a URL as a named dictionary.
    """
    raw_url = str(url).strip()

    if not (raw_url.startswith("http://") or raw_url.startswith("https://")):
        parsed_target = "http://" + raw_url
    else:
        parsed_target = raw_url

    parsed_url = urlparse(parsed_target)
    hostname = parsed_url.hostname or ""
    extracted = tldextract.extract(parsed_target)

    domain = extracted.domain.lower() if extracted.domain else ""
    subdomain = extracted.subdomain.lower() if extracted.subdomain else ""
    registered_domain = f"{extracted.domain}.{extracted.suffix}".lower() if extracted.domain and extracted.suffix else ""

    path = parsed_url.path or ""
    query = parsed_url.query or ""
    fragment = parsed_url.fragment or ""

    # Check for brand impersonation: Brand keyword in domain, but not the official domain
    brand_in_domain = any(brand in domain for brand in TARGET_BRANDS)
    is_official_domain = any(registered_domain == f"{brand}.com" or registered_domain == f"{brand}.org" for brand in TARGET_BRANDS)
    impersonation_flag = int(brand_in_domain and not is_official_domain)

    return {
        "url_length": len(raw_url),
        "dot_count": raw_url.count("."),
        "hyphen_count": raw_url.count("-"),
        "underscore_count": raw_url.count("_"),
        "slash_count": raw_url.count("/"),
        "question_count": raw_url.count("?"),
        "equal_count": raw_url.count("="),
        "at_count": raw_url.count("@"),
        "ampersand_count": raw_url.count("&"),
        "digit_count": sum(c.isdigit() for c in raw_url),
        "alpha_count": sum(c.isalpha() for c in raw_url),
        "is_https": int(raw_url.startswith("https://")),
        "has_ip": has_ip_address(hostname),
        "subdomain_count": len(subdomain.split(".")) if subdomain else 0,
        "has_suspicious_keywords": int(
            bool(
                re.search(
                    r"login|verify|account|update|secure|bank|signin|confirm|password",
                    raw_url.lower(),
                )
            )
        ),
        "hostname_length": len(hostname),
        "path_length": len(path),
        "query_length": len(query),
        "fragment_length": len(fragment),
        "parameter_count": len(query.split("&")) if query else 0,
        "colon_count": raw_url.count(":"),
        "semicolon_count": raw_url.count(";"),
        "comma_count": raw_url.count(","),
        "dollar_count": raw_url.count("$"),
        "percent_count": raw_url.count("%"),
        "tilde_count": raw_url.count("~"),
        "plus_count": raw_url.count("+"),
        "special_char_count": sum(1 for c in raw_url if not c.isalnum()),
        "entropy": calculate_entropy(raw_url),
        "brand_impersonation": impersonation_flag,  # <-- Crucial new feature!
    }