from playwright.sync_api import sync_playwright
import requests
import re

URL = "https://fwc26-resale-usd.tickets.fifa.com"

TARGET_PRICE = 100000

PUSHOVER_USER_KEY = "ugi2wnwf8mo4v7bw555xr441wxc6qo"
PUSHOVER_API_TOKEN = "a8mspr1u5d3o9fdbpwneek52ksiz2q"


def send(msg):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": "a8mspr1u5d3o9fdbpwneek52ksiz2q",
            "user": "ugi2wnwf8mo4v7bw555xr441wxc6qo",
            "message": msg,
            "title": "FIFA Monitor"
        }
    )


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # IMPORTANT: wait for real page load
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(12000)

        html = page.content()

        print("HTML length:", len(html))  # DEBUG

        prices = re.findall(r"\$(\d{3,5})", html)
        prices = [int(p) for p in prices if 200 <= int(p) <= 20000]

        lowest = min(prices) if prices else None

        print("Lowest price:", lowest)

        if lowest and lowest <= TARGET_PRICE:
            send(f"🔥 FIFA DROP: ${lowest}")


if __name__ == "__main__":
    main()
