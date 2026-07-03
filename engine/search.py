from typing import List, Dict

LONDON = [
    ("LHR", "London Heathrow"),
    ("LGW", "London Gatwick"),
    ("LTN", "London Luton"),
    ("STN", "London Stansted"),
]

PAKISTAN = [
    ("ISB", "Islamabad"),
    ("LHE", "Lahore"),
    ("KHI", "Karachi"),
]

HUBS = [
    ("IST", "Istanbul"),
    ("DXB", "Dubai"),
    ("AUH", "Abu Dhabi"),
    ("DOH", "Doha"),
    ("GYD", "Baku"),
]


def format_route(route):
    """Convert [(code,name), ...] → readable string"""
    return " → ".join([f"{name} ({code})" for code, name in route])


def generate_routes(departure: str, destination: str, max_stops: int = 1) -> List[Dict]:

    routes = []

    dep_airports = LONDON
    dest_airports = PAKISTAN

    # -------------------------
    # DIRECT ROUTES
    # -------------------------
    if max_stops >= 0:
        for d in dep_airports:
            for a in dest_airports:
                routes.append({
                    "price": 300 + hash(d[0] + a[0]) % 120,
                    "route": format_route([d, a]),
                    "stops": 0,
                    "journey": "6–8h",
                    "reason": "Direct flight (simple but usually more expensive)",
                    "book": f"https://www.google.com/search?q=flights+{d[0]}+to+{a[0]}"
                })

    # -------------------------
    # 1 STOP ROUTES
    # -------------------------
    if max_stops >= 1:
        for d in dep_airports:
            for h in HUBS:
                for a in dest_airports:
                    routes.append({
                        "price": 260 + hash(d[0] + h[0] + a[0]) % 160,
                        "route": format_route([d, h, a]),
                        "stops": 1,
                        "journey": "10–16h",
                        "reason": f"Split route via {h[1]} reduces cost via separate carriers",
                        "book": f"https://www.google.com/search?q=flights+{d[0]}+to+{h[0]}+to+{a[0]}"
                    })

    routes.sort(key=lambda x: x["price"])
    return routes