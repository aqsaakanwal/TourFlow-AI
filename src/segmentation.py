import pandas as pd


def calculate_visitor_segments(df):
    """
    Calculate visitor segment distribution.
    """

    segments = (
        df["visitor_type"]
        .value_counts()
        .reset_index()
    )

    segments.columns = [
        "visitor_segment",
        "visitors"
    ]

    return segments


def calculate_activity_profile(df):
    """
    Calculate tourism activity distribution.
    """

    activities = (
        df["activity_type"]
        .value_counts()
        .reset_index()
    )

    activities.columns = [
        "activity_type",
        "records"
    ]

    return activities


def calculate_segment_destination(df):
    """
    Analyze visitor segments across destinations.
    """

    segment_destination = pd.crosstab(
        df["visitor_type"],
        df["destination"]
    )

    return segment_destination
