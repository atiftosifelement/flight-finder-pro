import requests
from config import KIWI_API_KEY

AIRPORTS = {
    "London (All)": ["LHR", "LGW", "LTN", "STN"],
    "Pakistan (All)": ["ISB", "LHE", "KHI"]
}


def resolve(x):
    return AIRPORTS.get(x, [x])


def search_kiwi(fly_from, fly_to, date_from, max_stopovers, max_price):

    url = "https://tequila-api.kiwi.com/v2/search"

    headers = {"apikey": KIWI_API_KEY}

    params = {
        "fly_from": fly_from,
        "fly_to": fly_to,
        "date_from": date_from,
        "date_to": date_from,
        "curr": "GBP",
        "price_to": max_price,
        "max_stopovers": max_stopovers,
        "limit": 10
    }

    r = requests.get(url, headers=headers, params=params, timeout=20)
    data = r.json()

    return data.get("data", [])


def generate_routes(origin, destination, date_out, date_in, max_stops, max_price):

    origins = resolve(origin)
    destinations = resolve(destination)

    results = []

    for o in origins:
        for d in destinations:

            # ONE WAY OR RETURN LOGIC
            if date_in:

                out = search_kiwi(o, d, date_out, max_stops, max_price)
                ret = search_kiwi(d, o, date_in, max_stops, max_price)

                for f in out:
                    results.append(format_flight(f, o, d, max_stops))

                for f in ret:
                    results.append(format_flight(f, d, o, max_stops))

            else:

                flights = search_kiwi(o, d, date_out, max_stops, max_price)

                for f in flights:
                    results.append(format_flight(f, o, d, max_stops))

    results.sort(key=lambda x: x["price"] if x["price"] else 999999)
    return results


def format_flight(f, o, d, stops):

    return {
        "price": f.get("price"),
        "route": f"{o} → {d}",
        "duration": f.get("duration", {}).get("total", 0) // 3600,
        "stops": stops,
        "booking_link": f.get("deep_link")
    }