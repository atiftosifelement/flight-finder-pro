import streamlit as st
from engine.search import generate_routes

st.set_page_config(
    page_title="SplitFare AI",
    page_icon="✈️",
    layout="wide"
)

# -------------------------
# SESSION STATE
# -------------------------
if "selected_route" not in st.session_state:
    st.session_state.selected_route = None

if "results" not in st.session_state:
    st.session_state.results = []

# -------------------------
# HEADER
# -------------------------
st.title("✈️ SplitFare AI")
st.caption("Smart split-ticket flight search")

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.header("Search")

    departure = st.selectbox(
        "Departure",
        ["London", "Nearby London", "Any UK"]
    )

    destination = st.selectbox(
        "Destination",
        ["Pakistan", "Anywhere"]
    )

    max_stops = st.selectbox("Max Stops", [0, 1, 2])

    search = st.button("🔍 Search")

# -------------------------
# SEARCH
# -------------------------
if search:
    st.session_state.selected_route = None
    st.session_state.results = generate_routes(departure, destination, max_stops)

# -------------------------
# DETAIL VIEW
# -------------------------
def show_detail(route):
    st.subheader("🧭 Route Details")

    st.markdown(f"## 💰 £{route['price']}")
    st.markdown(f"## ✈️ {route['route']}")
    st.markdown(f"**Stops:** {route['stops']}")
    st.markdown(f"**Journey:** {route['journey']}")

    st.divider()

    st.markdown("### 🧠 Why this route?")
    st.write(route.get("reason", "Optimised route"))

    st.divider()

    book_link = route.get("book", None)

    if book_link:
        st.markdown(f"[🔗 Book this route]({book_link})")

    if st.button("⬅ Back"):
        st.session_state.selected_route = None
        st.rerun()

# -------------------------
# RESULTS
# -------------------------
if st.session_state.selected_route:
    show_detail(st.session_state.selected_route)

else:
    st.subheader("Results")

    if not st.session_state.results:
        st.info("Search to generate routes")
    else:
        for i, route in enumerate(st.session_state.results[:10]):

            st.markdown("---")

            col1, col2, col3 = st.columns([2, 3, 1])

            with col1:
                st.markdown(f"### £{route.get('price','-')}")

            with col2:
                st.markdown(f"✈️ {route.get('route','')}")
                st.caption(f"{route.get('stops',0)} stop(s) • {route.get('journey','')}")

            with col3:
                if st.button("View", key=f"v_{i}"):
                    st.session_state.selected_route = route
                    st.rerun()

                if "book" in route:
                    st.markdown(f"[Book]({route['book']})")