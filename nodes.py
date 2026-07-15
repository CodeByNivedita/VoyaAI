import json

from langchain_core.messages import SystemMessage, HumanMessage
from services.hotels import get_hotels
from llm import llm
from services.attractions import get_attractions
from langchain_core.messages import AIMessage
from services.routes import get_travel_details
from services.images import get_destination_images
import streamlit as st
from utils import safe_llm_invoke
from services.budget_engine import estimate_budget

from prompts import (
    EXTRACT_PROMPT,
    PLANNER_PROMPT,
    RESPONSE_PROMPT,
)

from schemas import (
    TravelDetails,
    PlannerOutput,
)
from schemas import ItineraryOutput
from prompts import ITINERARY_PROMPT
from services.weather import get_weather
import state


# Structured LLMs
structured_llm = llm.with_structured_output(TravelDetails)
planner_llm = llm.with_structured_output(PlannerOutput)
itinerary_llm = llm.with_structured_output(ItineraryOutput)


from langchain_core.messages import SystemMessage, HumanMessage

from langchain_core.messages import SystemMessage, HumanMessage

def extract_information(state):

    messages = state.get("messages", [])

    if not messages:
        messages = [HumanMessage(content=state["user_query"])]

    response = safe_llm_invoke(
        structured_llm,
        [SystemMessage(content=EXTRACT_PROMPT)] + messages,
    )

    if isinstance(response, dict) and not response.get("success", True):
        state["error"] = response["error"]
        return state

    state["travel_details"] = response

    state.setdefault("observations", {})

    return state

def planner(state):
    """
    Decide which tasks are required for the user's request.
    """

    details = state["travel_details"]

    response = safe_llm_invoke(
        planner_llm,
        [
            SystemMessage(content=PLANNER_PROMPT),
            HumanMessage(content=details.model_dump_json()),
        ],
    )

    # If the LLM call failed
    if isinstance(response, dict) and not response.get("success", True):
        state["error"] = response["error"]
        return state

    state["plan"] = response.tasks

    print("================================")
    print("Planner Tasks:", state["plan"])
    print("================================")

    return state
def weather_node(state):
    """
    Fetch weather for the extracted destination.
    """

    destination = state["travel_details"].destination

    if destination is None:
        state["observations"]["weather"] = {
            "error": "No destination found."
        }
        return state

    weather = get_weather(destination)

    state["observations"]["weather"] = weather

    return state


def hotel_node(state):
    """
    Fetch hotel recommendations.
    """

    destination = state["travel_details"].destination

    if destination is None:
        return state

    hotels = get_hotels(destination)

    state["observations"]["hotels"] = hotels

    return state


def attraction_node(state):
    """
    Fetch attractions for the destination.
    """

    destination = state["travel_details"].destination

    if destination is None:
        state["observations"]["attractions"] = []
        return state

    attractions = get_attractions(destination)

    state["observations"]["attractions"] = attractions

    return state


def route_node(state):
    print("========== ROUTE NODE ==========")

    travel = state["travel_details"]

    print("Departure:", travel.departure_city)
    print("Destination:", travel.destination)

    departure = travel.departure_city
    destination = travel.destination

    if not departure or not destination:
        print("Route skipped")
        state["observations"]["route"] = None
        return state

    route = get_travel_details(
        departure,
        destination
    )

    print("Generated Route:", route)

    state["observations"]["route"] = route

    print("Stored Route:", state["observations"]["route"])

    return state

def image_node(state):
    """
    Fetch destination images.
    """

    destination = state["travel_details"].destination

    if not destination:
        state["observations"]["images"] = []
        return state

    images = get_destination_images(destination)

    state["observations"]["images"] = images

    return state

def itinerary_node(state):
    """
    Generate a day-wise itinerary.
    """

    travel = state["travel_details"]
    observations = state["observations"]

    response = safe_llm_invoke(
        itinerary_llm,
        [
            SystemMessage(content=ITINERARY_PROMPT),
            HumanMessage(
                content=f"""
Travel Details:

{travel.model_dump_json(indent=2)}

Weather:

{observations.get("weather")}

Attractions:

{observations.get("attractions")}
"""
            ),
        ],
    )

    # If the LLM call failed
    if isinstance(response, dict) and not response.get("success", True):
        state["error"] = response["error"]
        return state

    state["observations"]["itinerary"] = [
        day.model_dump()
        for day in response.itinerary
    ]

    return state


def budget_node(state):

    travel = state["travel_details"]
    route = state["observations"].get("route", {})

    travel_options = route.get("travel_options", {})

    # Default fare
    fare_per_person = 0

    # Use preferred transport if available
    if (
        travel.transportation_preference
        and travel.transportation_preference in travel_options
    ):
        fare_per_person = travel_options[
            travel.transportation_preference
        ]["fare"]

    # Otherwise choose the cheapest option
    elif travel_options:
        fare_per_person = min(
            option["fare"]
            for option in travel_options.values()
        )

    budget = estimate_budget(
        travel,
        fare_per_person
    )

    state["observations"]["budget"] = budget

    return state

TOOLS = {
    "route": route_node,
    "weather": weather_node,
    "images": image_node,          
    "hotels": hotel_node,
    "attractions": attraction_node,
    "budget": budget_node,
    "itinerary": itinerary_node,
}

def executor_node(state):
    """
    Executes all required tools and stores their outputs
    in state["observations"].
    """

    if "observations" not in state or state["observations"] is None:
        state["observations"] = {}

    plan = state.get("plan", [])


    # Always generate these sections even if planner misses them
    required_tools = [
        "weather",
        "budget",
        "hotels",
        "attractions",
        "itinerary",
    ]

    # Merge planner output with required tools
    final_plan = []

    for task in plan:
        if task in TOOLS and task not in final_plan:
            final_plan.append(task)

    for task in required_tools:
        if task not in final_plan:
            final_plan.append(task)

    # Execute tools safely
    for task in final_plan:
        try:
            state = TOOLS[task](state)
        except Exception as e:
            print(f"[Executor] {task} failed: {e}")

            # Prevent frontend crashes
            if task not in state["observations"]:
                state["observations"][task] = None

    return state




def response_node(state):
    """
    Generate the final response using all collected observations.
    """

    travel = state["travel_details"]
    observations = state["observations"]

    context = f"""
Travel Details
--------------
Destination : {travel.destination}
Days        : {travel.number_of_days}
Budget      : ₹{travel.budget}

"""

    # -------------------------
    # Weather
    # -------------------------
    if observations.get("weather"):

        weather = observations["weather"]

        context += f"""
Weather
--------
Temperature : {weather.get('temperature')} °C
Condition   : {weather.get('condition')}
Description : {weather.get('description')}
Humidity    : {weather.get('humidity')}%
Wind Speed  : {weather.get('wind_speed')} m/s

"""

    # -------------------------
    # Hotels
    # -------------------------
    if observations.get("hotels"):

        context += "\nHotels\n------\n"

        for i, hotel in enumerate(observations["hotels"], start=1):

            context += f"""
{i}. {hotel["name"]}
   Category : {hotel["category"]}
   Address  : {hotel["address"]}
   Rooms    : {hotel["rooms"]}

"""

    # -------------------------
    # Attractions
    # -------------------------
    if observations.get("attractions"):

        context += "\nAttractions\n-----------\n"

        for i, place in enumerate(observations["attractions"], start=1):

            context += f"""
{i}. {place["name"]}
   Type        : {place["type"]}
   Rating      : {place["rating"]}
   Entry Fee   : ₹{place["entry_fee"]}
   Time Needed : {place["time_needed"]} hrs
   Best Time   : {place["best_time"]}

"""

    # -------------------------
    # Budget
    # -------------------------
    if observations.get("budget"):

        budget = observations["budget"]

        context += f"""
Budget
------
Total Budget      : ₹{budget["total_budget"]}
Daily Budget      : ₹{budget["daily_budget"]}
Hotel Budget      : ₹{budget["hotel_budget"]}
Food Budget       : ₹{budget["food_budget"]}
Transport Budget  : ₹{budget["transport_budget"]}
Activities Budget : ₹{budget["activities_budget"]}
Misc Budget       : ₹{budget["misc_budget"]}

"""

    # -------------------------
    # Itinerary
    # -------------------------
    if observations.get("itinerary"):

        context += f"""
Itinerary
---------
{observations["itinerary"]}

"""

    # -------------------------
    # Final Response
    # -------------------------

    response = safe_llm_invoke(
        llm,
        [
            SystemMessage(content=RESPONSE_PROMPT),
            HumanMessage(content=context),
        ],
    )

    if isinstance(response, dict) and not response.get("success", True):
        state["error"] = response["error"]
        return state

    state["final_answer"] = response.content

    state["dashboard"] = {
        "travel": state["travel_details"],
        "weather": observations.get("weather"),
        "images": observations.get("images", []),
        "budget": observations.get("budget"),
        "hotels": observations.get("hotels", []),
        "attractions": observations.get("attractions", []),
        "itinerary": observations.get("itinerary"),
        "route": observations.get("route"),
    }

    state["messages"].append(
        AIMessage(content=response.content)
    )

    return state