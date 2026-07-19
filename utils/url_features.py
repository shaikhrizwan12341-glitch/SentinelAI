import re
import ipaddress
from urllib.parse import urlparse

import tldextract


def has_ip_address(hostname: str) -> int:
    """
    Check whether the hostname is an IPv4 or IPv6 address.
    """
    try:
        ipaddress.ip_address(hostname)
        return 1
    except ValueError:
        return 0


def extract_url_features(url: str) -> list:
    """
    Extract numerical features from a URL.

    The feature order must remain consistent during:
    1. Model training
    2. Model prediction
    """

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname or ""

    extracted = tldextract.extract(url)

    features = [
        len(url),
        url.count("."),
        url.count("-"),
        url.count("_"),
        url.count("/"),
        url.count("?"),
        url.count("="),
        url.count("@"),
        url.count("&"),
        sum(character.isdigit() for character in url),
        sum(character.isalpha() for character in url),
        int(url.lower().startswith("https://")),
        has_ip_address(hostname),
        len(extracted.subdomain.split(".")) if extracted.subdomain else 0,
        int(bool(re.search(
            r"login|verify|account|update|secure|bank|signin|confirm|password",
            url.lower()
        ))),
    ]

    return features