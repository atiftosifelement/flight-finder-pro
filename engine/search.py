import requests
from config import KIWI_API_KEY

# -----------------------
# AIRPORT MAPPING
# -----------------------
AIRPORTS = {
    "London (All)": ["LHR", "LGW", "LTN", "STN"],
    "Pakistan (All)": ["ISB", "LHE", "KHI"]
}


def resolve_airports(code):
    return AIRPORTS.get(code, [code])


def search_kiwi(fly_from, fly_to, date_from, max_price):

    url = "https://tequila-api.kiwi.com/v2/search"

    headers = {
        "apikey": KIWI_API_KEY
    }

    params = {
        "fly_from": fly_from,
        "fly_to": fly_to,
        "date_from": date_from.strftime("%d/%m/%Y") if hasattr(date_from, "strftime") else date_from,
        "date_to": date_from.strftime("%d/%m/%Y") if hasattr(date_from, "strftime") else date_from,
        "curr": "GBP",
        "price_to": max_price,
        "limit": 10
    }

    r = requests.get(url, headers=headers, params=params, timeout=20)

    data = r.json()

    return data.get("data", [])


def generate_routes(origin, destination, date, max_price):

    origins = resolve_airports(origin)
    destinations = resolve_airports(destination)

    results = []

    for o in origins:
        for d in destinations:

            flights = search_kiwi(o, d, date, max_price)

            for f in flights:
                results.append({
                    "price": f.get("price"),
                    "route": f"{o} → {d}",
                    "airline": ", ".join(f.get("airlines", [])),
                    "duration": f.get("duration", {}).get("total", 0) // 3600,
                    "booking_link": f.get("deep_link")
                })

    results.sort(key=lambda x: x["price"] or 999999)
    return results