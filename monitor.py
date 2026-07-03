import requests
import re

URL = "https://fwc26-resale-usd.tickets.fifa.com"

TARGET_PRICE = 1000

PUSHOVER_USER_KEY = ugi2wnwf8mo4v7bw555xr441wxc6qo
PUSHOVER_API_TOKEN = a8mspr1u5d3o9fdbpwneek52ksiz2q


def send(message):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": "a8mspr1u5d3o9fdbpwneek52ksiz2q"
            "user": "ugi2wnwf8mo4v7bw555xr441wxc6qo"
            "message": message,
            "title": "FIFA Monitor"
        }
    )


def check_prices():
    html = requests.get(URL, timeout=20).text

    prices = re.findall(r"\$(\d{3,5})", html)
    prices = [int(p) for p in prices]

    return min(prices) if prices else None


def main():
    price = check_prices()

    if not price:
        print("No prices found")
        return

    print("Lowest price:", price)

    if price <= TARGET_PRICE:
        send(f"🔥 Brazil vs Norway drop: ${price}")


if __name__ == "__main__":
    main()
