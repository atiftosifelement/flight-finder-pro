import streamlit as st
from engine.search import generate_routes

st.set_page_config(page_title="SplitFare AI", layout="wide")

st.title("✈️ SplitFare AI (LIVE FLIGHTS)")

with st.sidebar:
    max_price = st.slider("Max Price (£)", 100, 2000, 800)
    search = st.button("Search Flights")

if "results" not in st.session_state:
    st.session_state.results = []

if search:
    st.session_state.results = generate_routes("London", "Pakistan", max_price)

st.subheader("Results")

if st.session_state.results:

    for f in st.session_state.results:

        st.markdown("---")

        st.markdown(f"### £{f.get('price','N/A')}")
        st.write(f.get("route", ""))
        st.write("✈️", f.get("airline", "Unknown"))
        st.write("⏱", f.get("duration", 0), "hours")

        link = f.get("booking_link")

        if link:
            st.markdown(f"[🔗 Book Flight]({link})")

else:
    st.info("Search to load live flights")