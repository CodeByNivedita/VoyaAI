import requests

from config import UNSPLASH_ACCESS_KEY

BASE_URL = "https://api.unsplash.com/search/photos"


def get_destination_images(destination: str, limit: int = 5):
    """
    Fetch destination images from Unsplash.

    Returns:
    [
        {
            "small": "...",
            "regular": "...",
            "full": "...",
            "photographer": "...",
            "link": "..."
        }
    ]
    """

    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }

    params = {
        "query": f"{destination} India landscape",
        "per_page": limit,
        "orientation": "landscape"
    }

    response = requests.get(
        BASE_URL,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    images = []

    for photo in data["results"]:

        images.append(
            {
                "small": photo["urls"]["small"],
                "regular": photo["urls"]["regular"],
                "full": photo["urls"]["full"],
                "photographer": photo["user"]["name"],
                "link": photo["links"]["html"],
            }
        )

    return images