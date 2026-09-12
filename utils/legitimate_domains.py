from urllib.parse import urlparse

import tldextract


TRUSTED_DOMAINS = {
    "google.com",
    "youtube.com",
    "youtu.be",
    "microsoft.com",
    "outlook.com",
    "office.com",
    "apple.com",
    "amazon.com",
    "facebook.com",
    "instagram.com",
    "github.com",
    "linkedin.com",
    "netflix.com",
    "paypal.com",
    "chase.com",
    "wellsfargo.com",
    "bankofamerica.com",
    "binance.com",
    "coinbase.com",
    "steampowered.com",
    "steamcommunity.com",
    "twitter.com",
    "x.com",
}


TARGET_BRANDS = {
    "paypal",
    "google",
    "youtube",
    "microsoft",
    "apple",
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
}


def normalize_hostname(url: str) -> str:
    """
    Normalize a URL and return its hostname.

    Examples:
        https://www.youtube.com -> www.youtube.com
        youtube.com/path -> youtube.com
    """
    value = url.strip()

    if "://" not in value:
        value = f"https://{value}"

    parsed = urlparse(value)
    hostname = parsed.hostname

    if not hostname:
        return ""

    return hostname.lower().rstrip(".")


def get_registered_domain(url: str) -> str:
    """
    Return the registered/root domain using the Public Suffix List.

    Examples:
        www.youtube.com -> youtube.com
        login.youtube.com -> youtube.com
        youtube.com.evil-site.com -> evil-site.com
    """
    hostname = normalize_hostname(url)

    if not hostname:
        return ""

    extracted = tldextract.extract(hostname)

    return extracted.top_domain_under_public_suffix.lower()


def is_trusted_domain(url: str) -> bool:
    """
    Return True only when the registered domain is explicitly trusted.

    This prevents malicious domains such as:
        youtube.com.evil-site.com
    from being treated as youtube.com.
    """
    registered_domain = get_registered_domain(url)

    return registered_domain in TRUSTED_DOMAINS


def get_brand_impersonation_flag(url: str) -> str | None:
    """
    Detect known-brand names being abused inside a non-trusted hostname.

    Examples:
        youtube.com.evil-site.com
        paypal.evil-site.com
        secure-login-google.evil.com

    Returns a security flag when brand impersonation is detected.
    """
    hostname = normalize_hostname(url)

    if not hostname:
        return None

    registered_domain = get_registered_domain(url)

    if not registered_domain:
        return None

    # Never flag an actually trusted registered domain.
    if registered_domain in TRUSTED_DOMAINS:
        return None

    hostname_parts = hostname.split(".")

    # Remove the registered domain components.
    registered_parts = registered_domain.split(".")

    if len(hostname_parts) <= len(registered_parts):
        return None

    subdomain_parts = hostname_parts[: -len(registered_parts)]

    # Check brand names appearing in the subdomain.
    for part in subdomain_parts:
        normalized_part = part.lower().replace("-", "").replace("_", "")

        for brand in TARGET_BRANDS:
            normalized_brand = brand.lower().replace("-", "").replace("_", "")

            if normalized_brand in normalized_part:
                return "Brand impersonation detected in subdomain"

    return None