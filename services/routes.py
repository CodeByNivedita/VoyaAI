import os
import requests

ORS_API_KEY = os.getenv("ORS_API_KEY")

GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"


def geocode_city(city: str):
    """
    Convert a city name into longitude and latitude.
    """

    headers = {
        "Authorization": ORS_API_KEY
    }

    params = {
        "text": city,
        "size": 1
    }

    response = requests.get(
        GEOCODE_URL,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    if not data["features"]:
        raise Exception(f"City '{city}' not found.")

    coordinates = data["features"][0]["geometry"]["coordinates"]

    return coordinates

DIRECTION_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


def get_route(departure_city: str, destination_city: str):
    """
    Return distance (km) and travel duration (hours)
    between two cities.
    """

    start = geocode_city(departure_city)
    end = geocode_city(destination_city)

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            start,
            end
        ]
    }

    response = requests.post(
        DIRECTION_URL,
        headers=headers,
        json=body
    )

    response.raise_for_status()

    data = response.json()

    summary = data["routes"][0]["summary"]

    distance = round(summary["distance"] / 1000, 2)

    duration = round(summary["duration"] / 3600, 2)

    return {
        "distance": distance,
        "duration": duration
    }

def estimate_travel_options(distance_km: float):
    """
    Estimate fare and travel time for different transport modes.
    """

    options = {
        "Car": {
            "fare": round(distance_km * 8),
            "duration": round(distance_km / 60, 1),
        },
        "Bus": {
            "fare": round(distance_km * 2),
            "duration": round(distance_km / 50, 1),
        },
        "Train": {
            "fare": round(distance_km * 1.4),
            "duration": round(distance_km / 55, 1),
        },
        "Flight": {
            "fare": round(2500 + distance_km * 4),
            "duration": round(distance_km / 550 + 2, 1),
        },
    }

    return options

def get_travel_details(
    departure_city: str,
    destination_city: str,
):
    """
    Complete journey information.
    """

    route = get_route(
        departure_city,
        destination_city,
    )

    options = estimate_travel_options(
        route["distance"]
    )

    return {
        "departure": departure_city,
        "destination": destination_city,
        "distance": route["distance"],
        "travel_options": options,
    }