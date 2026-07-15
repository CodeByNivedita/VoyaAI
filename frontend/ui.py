import streamlit as st

from frontend.components import (
    render_header,
    render_home,
    render_trip_summary,
    render_weather,
    render_budget,
    render_hotels,
    render_attractions,
    render_itinerary,
    render_success,
    render_footer
)


def show_home():
    render_home()


def show_dashboard(
    destination,
    days,
    budget,
    travelers,
    observations
):

    render_header()

    render_trip_summary(
        destination,
        days,
        budget,
        travelers
    )

    weather = observations.get("weather")
    budget_data = observations.get("budget")
    hotels = observations.get("hotels")
    attractions = observations.get("attractions")
    itinerary = observations.get("itinerary")

    left, right = st.columns([2, 1], gap="large")

    with left:
        render_weather(weather)
        render_attractions(attractions)

    with right:
        render_budget(budget_data)

    st.divider()

    render_hotels(hotels)

    st.divider()

    render_itinerary(itinerary)

    render_success(destination)

    render_footer()