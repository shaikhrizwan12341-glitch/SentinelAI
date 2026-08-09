from utils.predict_v2 import predict_url

test_urls = [
    "https://google.com",
    "https://github.com",
    "https://www.microsoft.com",
    "http://paypal-login-security-update.com",
]

print("=" * 60)
print("SentinelAI URL Model Test")
print("=" * 60)

for url in test_urls:
    print("\nURL:", url)

    result = predict_url(url)

    print("Prediction :", result["prediction"])
    print("Confidence :", result["confidence"])
    print("Phishing   :", result["phishing_probability"])
    print("Safe       :", result["safe_probability"])

    if "flag" in result:
        print("Flag       :", result["flag"])