from playwright.sync_api import sync_playwright
import requests
import re

URL = "https://fwc26-resale-usd.tickets.fifa.com"

TARGET_PRICE = 1500

PUSHOVER_USER_KEY = "YOUR_USER_KEY"
PUSHOVER_API_TOKEN = "YOUR_APP_TOKEN"


def send(msg):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_API_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "message": msg,
            "title": "FIFA Monitor"
        }
    )


def extract_prices(page):
    page.wait_for_timeout(8000)

    html = page.content()

    prices = re.findall(r"\$(\d{3,5})", html)
    prices = [int(p) for p in prices if 200 <= int(p) <= 20000]

    return min(prices) if prices else None


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL)

        price = extract_prices(page)

        browser.close()

        print("Lowest price:", price)

        if price and price <= TARGET_PRICE:
            send(f"🔥 FIFA DROP: ${price}")


if __name__ == "__main__":
    main()
