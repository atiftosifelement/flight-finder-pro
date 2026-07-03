import streamlit as st
from engine.search import generate_routes

st.set_page_config(
    page_title="SplitFare AI",
    page_icon="✈️",
    layout="wide"
)

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "selected_route" not in st.session_state:
    st.session_state.selected_route = None

# -----------------------------
# HEADER
# -----------------------------
st.title("✈️ SplitFare AI")
st.caption("Find cheaper flights using smart split routes")

# -----------------------------
# SIDEBAR SEARCH
# -----------------------------
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

    budget = st.slider("Budget (£)", 100, 2000, 700)

    search_clicked = st.button("🔍 Search")

# -----------------------------
# SEARCH RESULTS
# -----------------------------
if search_clicked:
    st.session_state.selected_route = None
    st.session_state.results = generate_routes(departure, destination, max_stops)

# -----------------------------
# ROUTE DETAIL VIEW (PAGE B)
# -----------------------------
def show_route_detail(route):
    st.subheader("🧭 Route Details")

    st.markdown(f"### 💰 £{route['price']}")
    st.markdown(f"### ✈️ {route['route']}")
    st.markdown(f"**Stops:** {route['stops']}")
    st.markdown(f"**Journey:** {route['journey']}")

    st.divider()

    st.markdown("## 🧠 Why this route?")
    st.write(route.get("reason", "Optimized for lowest cost and reasonable travel time."))

    st.divider()

    if st.button("⬅ Back to results"):
        st.session_state.selected_route = None

# -----------------------------
# RESULTS PAGE
# -----------------------------
if st.session_state.selected_route:
    show_route_detail(st.session_state.selected_route)

else:
    st.subheader("Results")

    if "results" not in st.session_state:
        st.info("Search to find flights")
    else:
        for i, route in enumerate(st.session_state.results[:10]):
            with st.container():
                st.markdown("---")

                col1, col2, col3 = st.columns([2, 2, 1])

                with col1:
                    st.markdown(f"### £{route['price']}")

                with col2:
                    st.markdown(f"✈️ {route['route']}")
                    st.caption(f"{route['stops']} stop(s) • {route['journey']}")

                with col3:
                    if st.button("View Details", key=f"btn_{i}"):
                        st.session_state.selected_route = route
                        st.rerun()