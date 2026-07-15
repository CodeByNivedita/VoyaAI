from services.budget_engine import estimate_budget


def get_current_budget(
    travel,
    route,
    selected_transport,
    selected_hotel,
):
    """
    Calculate the latest budget based on the
    user's selected transport and hotel.
    """

    # ---------------------------------
    # Transport
    # ---------------------------------

    fare = route["travel_options"][selected_transport]["fare"]

    # ---------------------------------
    # Hotel
    # ---------------------------------

    hotel_price = 2500

    if selected_hotel:

        hotel_price = selected_hotel["price_per_night"]

    # ---------------------------------
    # Estimate Budget
    # ---------------------------------

    return estimate_budget(
        travel=travel,
        fare_per_person=fare,
        hotel_price_per_night=hotel_price,
    )