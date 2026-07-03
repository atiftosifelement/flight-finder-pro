import streamlit as st
from engine.search import generate_routes

st.set_page_config(page_title="SplitFare AI", layout="wide")

st.title("✈️ SplitFare AI (LIVE SEARCH)")

# -----------------------
# INPUTS (NOW REAL)
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

    date = st.date_input("Departure Date")

    max_price = st.slider("Max Price (£)", 100, 2000, 800)

    search_btn = st.button("Search Flights")

# -----------------------
# STATE
# -----------------------
if "results" not in st.session_state:
    st.session_state.results = []

# -----------------------
# SEARCH ACTION
# -----------------------
if search_btn:
    st.session_state.results = generate_routes(
        origin,
        destination,
        str(date),
        max_price
    )

# -----------------------
# RESULTS
# -----------------------
st.subheader("Results")

if not st.session_state.results:
    st.info("Search to find live flights")
else:

    for f in st.session_state.results:

        st.markdown("---")

        st.markdown(f"### £{f.get('price','N/A')}")
        st.write("✈️ Route:", f.get("route"))
        st.write("✈️ Airline:", f.get("airline"))
        st.write("⏱ Duration:", f.get("duration"), "hours")

        link = f.get("booking_link")

        if link:
            st.markdown(f"[🔗 Book Flight]({link})")