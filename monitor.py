from playwright.sync_api import sync_playwright
import requests
import json

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
    captured_prices = []

    def handle_response(response):
        try:
            if "application/json" in response.headers.get("content-type", ""):
                data = response.json()

                text = json.dumps(data)

                # crude but effective extraction fallback
                import re
                prices = re.findall(r"\$(\d{3,5})", text)

                for p in prices:
                    captured_prices.append(int(p))
        except:
            pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.on("response", handle_response)

        page.goto(URL)
        page.wait_for_timeout(15000)

        browser.close()

    if not captured_prices:
        print("No prices found in network traffic")
        return

    lowest = min(captured_prices)

    print("Lowest price:", lowest)

    if lowest <= TARGET_PRICE:
        send(f"🔥 FIFA DROP: ${lowest}")


if __name__ == "__main__":
    main()
