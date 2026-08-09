import ipaddress
import math
import re
from collections import Counter
from urllib.parse import urlparse

import tldextract


# Brands frequently impersonated in phishing URLs
TARGET_BRANDS = [
    "paypal",
    "google",
    "apple",
    "microsoft",
    "amazon",
    "netflix",
    "facebook",
    "instagram",
    "chase",
    "wellsfargo",
    "bankofamerica",
    "binance",
    "coinbase",
    "steam",
    "linkedin",
    "twitter",
    "outlook",
]


def has_ip_address(hostname: str) -> int:
    """Check whether the hostname is an IPv4 or IPv6 address."""

    try:
        ipaddress.ip_address(hostname)
        return 1
    except ValueError:
        return 0


def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy of a string."""

    if not text:
        return 0.0

    counts = Counter(text)
    length = len(text)

    entropy = 0.0

    for count in counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return round(entropy, 4)


def extract_features(url: str) -> dict:
    """
    Extract the exact 30 URL features used by the SentinelAI model.

    IMPORTANT:
    The feature names must match models/feature_order.json exactly.
    """

    raw_url = str(url).strip()

    # Remove accidental Markdown link formatting if supplied
    markdown_match = re.match(
        r"^\[.*?\]\((https?://.*?)\)$",
        raw_url
    )

    if markdown_match:
        raw_url = markdown_match.group(1)

    # Handle escaped protocol
    raw_url = raw_url.replace("https\\://", "https://")
    raw_url = raw_url.replace("http\\://", "http://")

    # Add protocol when missing
    if not raw_url.startswith(("http://", "https://")):
        parsed_target = "http://" + raw_url
    else:
        parsed_target = raw_url

    parsed_url = urlparse(parsed_target)

    hostname = parsed_url.hostname or ""

    # tldextract
    extracted = tldextract.extract(parsed_target)

    domain = extracted.domain.lower() if extracted.domain else ""
    subdomain = extracted.subdomain.lower() if extracted.subdomain else ""

    registered_domain = ""

    if extracted.domain and extracted.suffix:
        registered_domain = (
            f"{extracted.domain}.{extracted.suffix}"
        ).lower()

    path = parsed_url.path or ""
    query = parsed_url.query or ""
    fragment = parsed_url.fragment or ""

    # --------------------------------------------------
    # Suspicious keyword detection
    # --------------------------------------------------

    suspicious_pattern = (
        r"login|verify|account|update|secure|bank|"
        r"signin|confirm|password"
    )

    has_suspicious_keywords = int(
        bool(
            re.search(
                suspicious_pattern,
                raw_url.lower()
            )
        )
    )

    # --------------------------------------------------
    # Brand impersonation detection
    # --------------------------------------------------

    brand_in_domain = any(
        brand in domain
        for brand in TARGET_BRANDS
    )

    official_domains = {
        "paypal.com",
        "google.com",
        "apple.com",
        "microsoft.com",
        "amazon.com",
        "netflix.com",
        "facebook.com",
        "instagram.com",
        "chase.com",
        "wellsfargo.com",
        "bankofamerica.com",
        "binance.com",
        "coinbase.com",
        "steam.com",
        "linkedin.com",
        "twitter.com",
        "outlook.com",
    }

    is_official_domain = (
        registered_domain in official_domains
    )

    brand_impersonation = int(
        brand_in_domain and not is_official_domain
    )

    # --------------------------------------------------
    # Feature extraction
    # --------------------------------------------------

    features = {

        "url_length": len(raw_url),

        "dot_count": raw_url.count("."),

        "hyphen_count": raw_url.count("-"),

        "underscore_count": raw_url.count("_"),

        "slash_count": raw_url.count("/"),

        "question_count": raw_url.count("?"),

        "equal_count": raw_url.count("="),

        "at_count": raw_url.count("@"),

        "ampersand_count": raw_url.count("&"),

        "digit_count": sum(
            c.isdigit() for c in raw_url
        ),

        "alpha_count": sum(
            c.isalpha() for c in raw_url
        ),

        "is_https": int(
            raw_url.lower().startswith("https://")
        ),

        "has_ip": has_ip_address(hostname),

        "subdomain_count": (
            len(subdomain.split("."))
            if subdomain
            else 0
        ),

        "has_suspicious_keywords": has_suspicious_keywords,

        "hostname_length": len(hostname),

        "path_length": len(path),

        "query_length": len(query),

        "fragment_length": len(fragment),

        "parameter_count": (
            len(query.split("&"))
            if query
            else 0
        ),

        "colon_count": raw_url.count(":"),

        "semicolon_count": raw_url.count(";"),

        "comma_count": raw_url.count(","),

        "dollar_count": raw_url.count("$"),

        "percent_count": raw_url.count("%"),

        "tilde_count": raw_url.count("~"),

        "plus_count": raw_url.count("+"),

        "special_char_count": sum(
            1 for c in raw_url
            if not c.isalnum()
        ),

        "entropy": calculate_entropy(raw_url),

        "brand_impersonation": brand_impersonation,
    }

    return features