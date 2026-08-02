from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import tldextract
import ipaddress


# -----------------------------
# Helper Functions
# -----------------------------

def is_ip(domain):
    try:
        ipaddress.ip_address(domain)
        return 1
    except:
        return 0


def safe_request(url):

    try:
        headers = {
            "User-Agent":
            "Mozilla/5.0"
        }

        response = requests.get(
            url,
            timeout=10,
            headers=headers
        )

        return response

    except:

        return None


# -----------------------------
# Feature Extraction
# -----------------------------

def extract_features(url):

    parsed = urlparse(url)

    ext = tldextract.extract(url)

    domain = parsed.netloc

    response = safe_request(url)

    soup = None

    if response:

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

    features = {}

    # --------------------------
    # URL Features
    # --------------------------

    features["URLLength"] = len(url)

    features["DomainLength"] = len(domain)

    features["IsDomainIP"] = is_ip(domain)

    features["NoOfSubDomain"] = (
        len(ext.subdomain.split("."))
        if ext.subdomain
        else 0
    )

    features["IsHTTPS"] = (
        1
        if parsed.scheme == "https"
        else 0
    )

    # --------------------------
    # HTML Features
    # --------------------------

    if soup:

        title = soup.title.string if soup.title else ""

        features["HasTitle"] = int(bool(title))

        features["HasFavicon"] = int(
            soup.find("link", rel=lambda x: x and "icon" in x.lower()) is not None
        )

        features["HasDescription"] = int(
            soup.find("meta", attrs={"name": "description"}) is not None
        )

        features["HasPasswordField"] = len(
            soup.find_all("input", {"type": "password"})
        )

        features["HasSubmitButton"] = len(
            soup.find_all(
                "input",
                {"type": "submit"}
            )
        ) + len(
            soup.find_all("button")
        )

        features["HasHiddenFields"] = len(
            soup.find_all(
                "input",
                {"type": "hidden"}
            )
        )

        features["NoOfImage"] = len(
            soup.find_all("img")
        )

        features["NoOfCSS"] = len(
            soup.find_all("link")
        )

        features["NoOfJS"] = len(
            soup.find_all("script")
        )

        features["NoOfiFrame"] = len(
            soup.find_all("iframe")
        )

        features["NoOfPopup"] = response.text.lower().count("window.open")

        features["LineOfCode"] = len(
            response.text.splitlines()
        )

    else:

        features["HasTitle"] = 0
        features["HasFavicon"] = 0
        features["HasDescription"] = 0
        features["HasPasswordField"] = 0
        features["HasSubmitButton"] = 0
        features["HasHiddenFields"] = 0
        features["NoOfImage"] = 0
        features["NoOfCSS"] = 0
        features["NoOfJS"] = 0
        features["NoOfiFrame"] = 0
        features["NoOfPopup"] = 0
        features["LineOfCode"] = 0

    return features