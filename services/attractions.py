import pandas as pd

# Load once
attractions_df = pd.read_csv("data/attractions.csv")


def get_attractions(city: str, limit: int = 5):
    """
    Return top attractions for a given city.
    """

    results = attractions_df[
        attractions_df["City"].str.lower() == city.lower()
    ]

    if results.empty:
        return []

    attractions = []

    for _, row in results.head(limit).iterrows():

        attractions.append(
            {
                "name": row["Name"],
                "type": row["Type"],
                "rating": row["Google review rating"],
                "time_needed": row["time needed to visit in hrs"],
                "entry_fee": row["Entrance Fee in INR"],
                "best_time": row["Best Time to visit"],
                "significance": row["Significance"],
            }
        )

    return attractions