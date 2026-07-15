from math import ceil





def estimate_budget(
    travel,
    fare_per_person: int,
    hotel_price_per_night: int = 2500,
):
    """
    Estimate complete trip budget.
    """

    # ----------------------------------
    # Basic Details
    # ----------------------------------

    travelers = travel.number_of_travelers or 1
    days = travel.number_of_days or 1

    # ----------------------------------
    # Trip Type
    # ----------------------------------

    trip_multiplier = (
        2
        if travel.trip_type == "Round Trip"
        else 1
    )

    # ----------------------------------
    # Hotel
    # ----------------------------------

    rooms = ceil(travelers / 2)

    nights = max(days - 1, 1)

    hotel_budget = (
        hotel_price_per_night
        * rooms
        * nights
    )

    # ----------------------------------
    # Food
    # ----------------------------------

    food_per_person_per_day = 700

    food_budget = (
        food_per_person_per_day
        * travelers
        * days
    )

    # ----------------------------------
    # Transport
    # ----------------------------------

    transport_budget = (
        fare_per_person
        * travelers
        * trip_multiplier
    )

    # ----------------------------------
    # Activities
    # ----------------------------------

    activity_per_person = 1000

    activities_budget = (
        activity_per_person
        * travelers
    )

    # ----------------------------------
    # Shopping
    # ----------------------------------

    shopping_budget = int(
        0.10
        * (
            hotel_budget
            + food_budget
            + transport_budget
            + activities_budget
        )
    )

    # ----------------------------------
    # Misc
    # ----------------------------------

    misc_budget = int(
        0.05
        * (
            hotel_budget
            + food_budget
            + transport_budget
            + activities_budget
        )
    )

    # ----------------------------------
    # Total
    # ----------------------------------

    total_budget = (
        hotel_budget
        + food_budget
        + transport_budget
        + activities_budget
        + shopping_budget
        + misc_budget
    )

    daily_budget = round(
        total_budget / days
    )

    # ----------------------------------
    # Budget Status
    # ----------------------------------

    user_budget = travel.budget or total_budget

    difference = user_budget - total_budget

    if difference >= 0:

        budget_status = "Within Budget"

    else:

        budget_status = "Over Budget"

    # ----------------------------------
    # Suggestions
    # ----------------------------------

    suggestions = []

    if budget_status == "Over Budget":

        if transport_budget > 5000:
            suggestions.append(
                "Choose Train or Bus instead of Flight."
            )

        if hotel_budget > 10000:
            suggestions.append(
                "Select a lower hotel category."
            )

        if days > 5:
            suggestions.append(
                "Reduce the trip by one day."
            )

        if shopping_budget > 3000:
            suggestions.append(
                "Reduce shopping expenses."
            )

    # ----------------------------------
    # Return
    # ----------------------------------

    return {

        "hotel_budget": hotel_budget,

        "food_budget": food_budget,

        "transport_budget": transport_budget,

        "activities_budget": activities_budget,

        "shopping_budget": shopping_budget,

        "misc_budget": misc_budget,

        "daily_budget": daily_budget,

        "total_budget": total_budget,

        "rooms": rooms,

        "nights": nights,

        "fare_per_person": fare_per_person,

        "trip_multiplier": trip_multiplier,

        "hotel_price_per_night": hotel_price_per_night,

        "difference": difference,

        "budget_status": budget_status,

        "suggestions": suggestions,
    }