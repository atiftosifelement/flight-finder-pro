import streamlit as st

st.set_page_config(
    page_title="SplitFare AI",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ SplitFare AI")
st.caption("Find the cheapest flights using nearby airports, flexible dates and split tickets.")

with st.sidebar:
    st.header("Search")

    departure = st.selectbox(
        "Departure",
        [
            "London Airports",
            "Nearby London",
            "Any UK",
            "Custom"
        ]
    )

    destination = st.selectbox(
        "Destination",
        [
            "Pakistan",
            "Anywhere",
            "Custom"
        ]
    )

    date_mode = st.radio(
        "Date Mode",
        [
            "Fixed",
            "Flexible"
        ]
    )

    depart = st.date_input("Departure Date")

    returning = st.date_input("Return Date")

    budget = st.slider(
        "Maximum Budget (£)",
        100,
        2000,
        700
    )

    stops = st.selectbox(
        "Maximum Stops",
        [0,1,2]
    )

    bags = st.selectbox(
        "Checked Bags",
        [
            "Cabin Only",
            "23kg",
            "32kg"
        ]
    )

    search = st.button("🔍 Search Flights")

st.subheader("Results")

from engine.search import generate_routes

if search:
    results = generate_routes(departure, destination, stops)

    st.subheader("Results")

    st.dataframe(
        results,
        use_container_width=True
    )

st.dataframe(
    {
        "Price":["£341","£356","£372"],
        "Route":[
            "LTN → MXP → ISB",
            "STN → GYD → LHE",
            "LGW → AUH → ISB"
        ],
        "Stops":[1,1,1],
        "Journey":[
            "14h",
            "15h",
            "13h"
        ]
    },
    use_container_width=True
)