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


def format_route(route_list):
    return " → ".join([f"{name} ({code})" for code, name in route_list])


def generate_routes(departure, destination, max_stops=1):

    routes = []

    dep_airports = LONDON
    dest_airports = PAKISTAN

    # ------------------------
    # Direct flights
    # ------------------------
    if max_stops >= 0:
        for d in dep_airports:
            for a in dest_airports:
                routes.append({
                    "price": 300 + hash(d[0] + a[0]) % 120,
                    "route": format_route([d, a]),
                    "stops": 0,
                    "journey": "6–8h",
                    "reason": "Direct routing (simple but usually more expensive)",
                    "book": f"https://www.google.com/search?q=flights+{d[0]}+to+{a[0]}"
                })

    # ------------------------
    # 1-stop routes
    # ------------------------
    if max_stops >= 1:
        for d in dep_airports:
            for h in HUBS:
                for a in dest_airports:
                    routes.append({
                        "price": 260 + hash(d[0] + h[0] + a[0]) % 160,
                        "route": format_route([d, h, a]),
                        "stops": 1,
                        "journey": "10–16h",
                        "reason": f"Split ticket via {h[1]} reduces pricing via separate carriers",
                        "book": f"https://www.google.com/search?q=flights+{d[0]}+to+{h[0]}+to+{a[0]}"
                    })

    routes.sort(key=lambda x: x["price"])
    return routes