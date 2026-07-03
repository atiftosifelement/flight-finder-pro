import streamlit as st
from engine.search import generate_routes

st.set_page_config(page_title="SplitFare AI", layout="wide")

st.title("✈️ SplitFare AI (LIVE FLIGHTS)")

# -----------------------
# RESET BUTTON (FIX YOUR "RETURN OPTION")
# -----------------------
if st.button("🔄 Reset Search"):
    st.session_state.clear()
    st.rerun()

# -----------------------
# INPUTS
# -----------------------
with st.sidebar:

    st.header("Search")

    origin = st.selectbox(
        "From",
        ["London (All)", "LHR", "LGW", "LTN", "STN"]
    )

    destination = st.selectbox(
        "To",
        ["Pakistan (All)", "ISB", "LHE", "KHI"]
    )

    date = st.date_input("Date")

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
        str(date),
        max_price
    )

# -----------------------
# RESULTS
# -----------------------
st.subheader("Results")

if search:
    if not st.session_state.results:
        st.warning("⚠️ No flights found. Try different date or airports.")
    else:
        st.success(f"Found {len(st.session_state.results)} flights")

for f in st.session_state.results:

    st.markdown("---")

    st.markdown(f"### £{f.get('price','N/A')}")
    st.write("✈️", f.get("route"))
    st.write("✈️", f.get("airline"))
    st.write("⏱", f.get("duration"), "hours")

    if f.get("booking_link"):
        st.markdown(f"[🔗 Book Flight]({f['booking_link']})")