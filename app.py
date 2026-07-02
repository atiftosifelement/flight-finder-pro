import streamlit as st
from config import *

st.title("Flight Finder Pro")

st.write("Basic setup working")

st.subheader("Departure Airports")

st.checkbox("London Airports", True)
st.checkbox("Nearby Airports", True)

st.subheader("Destinations")

for d in DESTINATIONS:
    st.checkbox(d, True)

st.number_input("Max Budget (£)", value=700)

if st.button("Search Flights"):
    st.write("Engine not connected yet — next step")
