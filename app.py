import streamlit as st
from graph import graph
import traceback
from langchain_core.messages import HumanMessage

from frontend.components import (
    load_css,
    render_dashboard,
    render_navbar,
    render_hero,
    render_trip_banner,
    render_journey,
    render_weather, 
    render_budget,
    render_footer,
    render_loading,
)
import frontend.components


print(frontend.components.__file__)
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="VoyaAI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------

load_css()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "trip_data" not in st.session_state:
    st.session_state.trip_data = None

# --------------------------------------------------
# NAVBAR
# --------------------------------------------------

render_navbar()

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

trip_request = render_hero()

# --------------------------------------------------
# GENERATE TRIP
# --------------------------------------------------

if trip_request:

    with st.spinner("Generating your AI trip..."):

        render_loading()

        try:
            response = graph.invoke(
                {
                    "messages": [HumanMessage(content=trip_request)],
                    "user_query": trip_request,
                    "travel_details": None,
                    "plan": [],
                    "current_task": "",
                    "observations": {},
                    "final_answer": "",
                    "dashboard": {},
                    "error": None,
                }
            )

            st.session_state.trip_data = response
            st.rerun()

        except Exception as e:

            error_msg = str(e).lower()

            if "429" in error_msg or "quota" in error_msg:
                st.error(
                    "⚠️ API usage limit has been reached. Please try again later."
                )

            elif "401" in error_msg or "unauthorized" in error_msg:
                st.error(
                    "⚠️ Authentication failed. Please contact the application owner."
                )

            elif "timeout" in error_msg:
                st.error(
                    "⚠️ The request timed out. Please try again in a few moments."
                )

            elif "connection" in error_msg or "network" in error_msg:
                st.error(
                    "⚠️ Unable to connect to the required services. Please try again later."
                )

            else:
                st.error(
                    "⚠️ Sorry! We couldn't generate your travel plan right now. Please try again later."
                )

            # Log the actual error to the server logs (not shown to users)
            print(f"Application Error: {e}")
        

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if st.session_state.trip_data is not None:

    data = st.session_state.trip_data

    render_trip_banner(data)

    dashboard = data["dashboard"]

    route = dashboard.get("route")
    weather = dashboard.get("weather")
    budget = dashboard.get("budget")
    travel = dashboard.get("travel")

    if route:
        render_journey(route,travel)

    st.divider()

    if weather:
        render_weather(weather)

    st.divider()
    
    if budget:
        render_budget(budget,route,travel)

    st.divider()

    render_dashboard(data)

# --------------------------------------------------
# FOOTER
# ----------------------- ---------------------------

render_footer()