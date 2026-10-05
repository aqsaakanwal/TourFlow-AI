import pandas as pd


def calculate_tourism_flows(df):
    """
    Calculate origin-destination tourism flows.
    """

    flows = (
        df.groupby(["origin", "destination"])
        .size()
        .reset_index(name="trips")
        .sort_values("trips", ascending=False)
    )

    return flows


def calculate_destination_activity(df):
    """
    Calculate tourism activity for each destination.
    """

    activity = (
        df["destination"]
        .value_counts()
        .reset_index()
    )

    activity.columns = [
        "destination",
        "tourism_records"
    ]

    return activity


def get_top_destination(df):
    """
    Identify the destination with the highest tourism activity.
    """

    return df["destination"].value_counts().idxmax()


def get_destination_coordinates(df):
    """
    Extract unique geographic coordinates for destinations.
    """

    coordinates = (
        df[
            [
                "destination",
                "latitude",
                "longitude"
            ]
        ]
        .drop_duplicates(subset=["destination"])
        .reset_index(drop=True)
    )

    return coordinates


def get_origin_coordinates(df):
    """
    Provide geographic coordinates for tourism origins.
    """

    origin_coordinates = {
        "Lahore": {
            "latitude": 31.5204,
            "longitude": 74.3587
        },
        "Islamabad": {
            "latitude": 33.6844,
            "longitude": 73.0479
        }
    }

    origins = pd.DataFrame(
        [
            {
                "origin": origin,
                "latitude": values["latitude"],
                "longitude": values["longitude"]
            }
            for origin, values in origin_coordinates.items()
        ]
    )

    return origins
