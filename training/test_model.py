from utils.predict_v2 import predict_url

urls = [
    "https://google.com",
    "https://github.com",
    "http://paypal-login-security-update.com"
]

for url in urls:

    print("=" * 60)

    print(url)

    print(predict_url(url))