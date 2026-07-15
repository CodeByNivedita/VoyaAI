def estimate_budget(days: int, budget: int | None):
    """
    Estimate daily budget distribution.
    """

    if days is None or days <= 0:
        return {}

    if budget is None:
        budget = 5000 * days

    return {
        "total_budget": budget,
        "hotel_budget": int(budget * 0.40),
        "food_budget": int(budget * 0.20),
        "transport_budget": int(budget * 0.15),
        "activities_budget": int(budget * 0.20),
        "misc_budget": int(budget * 0.05),
        "daily_budget": int(budget / days),
    }