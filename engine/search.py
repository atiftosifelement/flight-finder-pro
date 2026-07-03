import requests
from config import KIWI_API_KEY

LONDON_AIRPORTS = ["LHR", "LGW", "LTN", "STN"]
PAKISTAN_AIRPORTS = ["ISB", "LHE", "KHI"]


def get_airports(region):
    if "London" in region:
        return LONDON_AIRPORTS
    if "Pakistan" in region:
        return PAKISTAN_AIRPORTS
    return [region]


def search_kiwi(fly_from, fly_to, date_from, max_price=2000):
    headers = {"apikey": KIWI_API_KEY}

    params = {
        "fly_from": fly_from,
        "fly_to": fly_to,
        "date_from": date_from,
        "date_to": date_from,
        "curr": "GBP",
        "price_to": max_price,
        "limit": 10
    }

    r = requests.get(
        "https://tequila-api.kiwi.com/v2/search",
        headers=headers,
        params=params
    )

    return r.json().get("data", [])


def generate_routes(departure, destination, max_price=2000):

    dep_airports = get_airports(departure)
    dest_airports = get_airports(destination)

    results = []

    for d in dep_airports:
        for a in dest_airports:

            flights = search_kiwi(d, a, "01/08/2026", max_price)

            for f in flights:
                results.append({
                    "price": f.get("price"),
                    "route": f"{d} → {a}",
                    "airline": ", ".join(f.get("airlines", [])),
                    "duration": f.get("duration", {}).get("total", 0) // 3600,
                    "booking_link": f.get("deep_link")
                })

    results.sort(key=lambda x: x["price"])
    return results