import streamlit as st
from engine.search import generate_routes

st.set_page_config(page_title="SplitFare AI", layout="wide")

st.title("✈️ SplitFare AI (LIVE FLIGHT SEARCH)")

# -----------------------
# RESET
# -----------------------
if st.button("🔄 Reset"):
    st.session_state.clear()
    st.rerun()

# -----------------------
# INPUTS
# -----------------------
with st.sidebar:

    st.header("Search Flights")

    origin = st.selectbox(
        "From",
        ["London (All)", "LHR", "LGW", "LTN", "STN"]
    )

    destination = st.selectbox(
        "To",
        ["Pakistan (All)", "ISB", "LHE", "KHI"]
    )

    trip_type = st.radio(
        "Trip Type",
        ["One Way", "Return"]
    )

    date_out = st.date_input("Departure Date")

    date_in = None
    if trip_type == "Return":
        date_in = st.date_input("Return Date")

    max_stops = st.selectbox(
        "Max Stops",
        [0, 1, 2]
    )

    max_price = st.slider("Max Price (£)", 100, 2000, 800)

    search = st.button("Search Flights")

# -----------------------
# STATE
# -----------------------
if "results" not in st.session_state:
    st.session_state.results = []

# -----------------------
# SEARCH
# -----------------------
if search:
    st.session_state.results = generate_routes(
        origin,
        destination,
        str(date_out),
        str(date_in) if date_in else None,
        max_stops,
        max_price
    )

# -----------------------
# RESULTS
# -----------------------
st.subheader("Results")

if not st.session_state.results:
    st.info("No results yet — try different date or increase stops.")
else:

    st.success(f"Found {len(st.session_state.results)} flights")

    for f in st.session_state.results:

        st.markdown("---")

        st.markdown(f"### £{f.get('price','N/A')}")
        st.write("✈️ Route:", f.get("route"))
        st.write("⏱ Duration:", f.get("duration"))
        st.write("🛑 Stops:", f.get("stops"))

        if f.get("booking_link"):
            st.markdown(f"[🔗 Book Flight]({f['booking_link']})")