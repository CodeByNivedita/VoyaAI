import pandas as pd

# Load once when the application starts
hotels_df = pd.read_csv("data/hotels.csv")
CATEGORY_PRICE = {
    "1 Star": 1500,
    "2 Star": 2500,
    "3 Star": 4000,
    "4 Star": 6500,
    "5 Star": 10000,
}

def get_hotels(city: str, limit: int = 5):
    """
    Return hotels for the given city.
    """

    results = hotels_df[
        hotels_df["City"].str.lower() == city.lower()
    ]

    if results.empty:
        return []

    hotels = []

    hotels = []

    for _, row in results.head(limit).iterrows():

      category = str(row["Category"]).strip()

      price = CATEGORY_PRICE.get(
        category,
        3500,          # default
      )

      hotels.append(
         {
            "name": row["Hotel Name"],
            "category": category,
            "address": row["Address"],
            "rooms": row["Total Rooms"],
            "price_per_night": price,
        }
      )

    return hotels