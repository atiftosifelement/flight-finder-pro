import streamlit as st
from engine.search import generate_routes

st.set_page_config(page_title="SplitFare AI", layout="wide")

st.title("✈️ SplitFare AI (LIVE FLIGHTS)")

with st.sidebar:
    departure = st.selectbox("From", ["London"])
    destination = st.selectbox("To", ["Pakistan"])
    max_price = st.slider("Max Price", 100, 2000, 800)

    search = st.button("Search Flights")

if "results" not in st.session_state:
    st.session_state.results = []

if search:
    st.session_state.results = generate_routes(departure, destination, max_price)

st.subheader("Results")

if st.session_state.results:

    for f in st.session_state.results:

        st.markdown("---")

        st.markdown(f"### £{f['price']}")
        st.write(f["route"])
        st.write("✈️", f.get("airline", "Unknown"))
        st.write("⏱", f.get("duration", 0), "hours")

        if f.get("booking_link"):
            st.markdown(f"[🔗 Book Flight]({f['booking_link']})")

else:
    st.info("Search to see live flights")