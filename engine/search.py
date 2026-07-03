import requests
from config import KIWI_API_KEY

AIRPORTS = {
    "London (All)": ["LHR", "LGW", "LTN", "STN"],
    "Pakistan (All)": ["ISB", "LHE", "KHI"]
}


def resolve(code):
    return AIRPORTS.get(code, [code])


def search_kiwi(fly_from, fly_to, date_from, max_price):

    url = "https://tequila-api.kiwi.com/v2/search"

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

    try:
        r = requests.get(url, headers=headers, params=params, timeout=20)
        data = r.json()

        # DEBUG SAFETY
        if "data" not in data:
            print("KIWI RESPONSE ERROR:", data)
            return []

        return data["data"]

    except Exception as e:
        print("API FAILED:", e)
        return []


def generate_routes(origin, destination, date, max_price):

    origins = resolve(origin)
    destinations = resolve(destination)

    results = []

    for o in origins:
        for d in destinations:

            flights = search_kiwi(o, d, date, max_price)

            for f in flights:
                results.append({
                    "price": f.get("price", 0),
                    "route": f"{o} → {d}",
                    "airline": ", ".join(f.get("airlines", [])),
                    "duration": f.get("duration", {}).get("total", 0) // 3600,
                    "booking_link": f.get("deep_link")
                })

    results.sort(key=lambda x: x["price"])
    return results