from typing import Optional
from pydantic import BaseModel, Field
from typing import List

class PlannerOutput(BaseModel):
    tasks: List[str]

class TravelDetails(BaseModel):
    """Structured travel information extracted from the user's query."""

    destination: Optional[str] = Field(
        default=None,
        description="Travel destination or city"
    )

    number_of_days: Optional[int] = Field(
        default=None,
        description="Trip duration in days"
    )

    budget: Optional[int] = Field(
        default=None,
        description="Total travel budget"
    )

    travel_month: Optional[str] = Field(
        default=None,
        description="Month of travel"
    )

    

    number_of_travelers: Optional[int] = Field(
        default=None,
        description="Total travelers"
    )

    trip_type: str | None = Field(
    default="Round Trip",
    description="Round Trip or One Way"
)
    transportation_preference: Optional[str] = Field(
        default=None,
        description="Flight, Train, Bus, Car, etc."
    )

    travel_class: str | None = Field(
    default="Economy",
    description="Economy, Business, First Class"
)
    departure_city: str | None = Field(
    default=None,
    description="City from where the journey starts"
    )

    travel_mode: str | None = Field(
    default="Car",
    description="Flight, Train, Bus or Car"
    )


class ItineraryDay(BaseModel):
    day: int = Field(description="Day number")
    morning: str = Field(description="Morning activity")
    afternoon: str = Field(description="Afternoon activity")
    evening: str = Field(description="Evening activity")
    estimated_cost: int = Field(description="Estimated cost for the day")


class ItineraryOutput(BaseModel):
    itinerary: list[ItineraryDay]

class BudgetOutput(BaseModel):

    hotel_budget: int

    food_budget: int

    transport_budget: int

    activities_budget: int

    shopping_budget: int

    misc_budget: int

    daily_budget: int

    total_budget: int

    rooms: int

    nights: int

    fare_per_person: int

    trip_multiplier: int

    hotel_price_per_night: int

    difference: int

    budget_status: str

    suggestions: list[str]