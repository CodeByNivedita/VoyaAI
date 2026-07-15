import pandas as pd

attractions_df = pd.read_csv("data/attractions.csv")
hotels_df = pd.read_csv("data/hotels.csv")

print(attractions_df.head())
print(hotels_df.head())
def get_attractions(city):
    city = city.lower()

    df = attractions_df[
        attractions_df["City"].str.lower() == city
    ]

    if df.empty:
        return []

    df = df.sort_values(
        by="Google review rating",
        ascending=False
    )

    return df.head(5).to_dict(orient="records")
def get_hotels(city):
    city = city.lower()

    df = hotels_df[
        hotels_df["City"].str.lower() == city
    ]

    if df.empty:
        return []

    return df.head(5).to_dict(orient="records")

    