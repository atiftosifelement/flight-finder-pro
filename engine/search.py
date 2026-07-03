from itertools import product

# London airport system
LONDON_AIRPORTS = ["LHR", "LGW", "LTN", "STN", "LCY", "SEN"]

# Pakistan airports
PAKISTAN_AIRPORTS = ["ISB", "LHE", "KHI", "PEW", "SKT"]

def get_airports(region: str):
    region = region.lower()

    if "london" in region:
        return LONDON_AIRPORTS

    if "pakistan" in region:
        return PAKISTAN_AIRPORTS

    return [region]


def generate_routes(departure: str, destination: str, max_stops: int = 1):
    """
    Generates simple split routes.
    This is NOT real flight data yet — just logic engine.
    """

    dep_airports = get_airports(departure)
    dest_airports = get_airports(destination)

    routes = []

    # direct routes (0 stops)
    if max_stops >= 0:
        for d in dep_airports:
            for a in dest_airports:
                routes.append({
                    "price": 300 + hash(d + a) % 120,
                    "route": f"{d} → {a}",
                    "stops": 0,
                    "journey": "6-8h"
                })

    # 1-stop routes (split logic)
    if max_stops >= 1:
        hubs = ["DXB", "AUH", "IST", "DOH", "GYD"]

        for d in dep_airports:
            for h in hubs:
                for a in dest_airports:
                    routes.append({
                        "price": 280 + hash(d + h + a) % 150,
                        "route": f"{d} → {h} → {a}",
                        "stops": 1,
                        "journey": "10-16h"
                    })

    # sort cheapest first
    routes.sort(key=lambda x: x["price"])

    return routes