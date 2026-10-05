def pressure_category(score):
    """
    Classify destination sustainability pressure.
    """

    if score >= 75:
        return "High"

    elif score >= 50:
        return "Moderate"

    else:
        return "Lower"


def calculate_sustainability_pressure(df):
    """
    Calculate prototype tourism pressure indicators
    for each destination.
    """

    sustainability = (
        df.groupby("destination")
        .agg(
            tourism_records=("visitor_id", "count"),
            average_stay=("stay_days", "mean"),
            adventure_activity=(
                "activity_type",
                lambda x: x.isin(
                    ["Trekking", "Hiking"]
                ).sum()
            )
        )
        .reset_index()
    )

    # Normalize tourism activity
    sustainability["activity_pressure"] = (
        sustainability["tourism_records"]
        / sustainability["tourism_records"].max()
    )

    # Normalize average stay
    sustainability["stay_pressure"] = (
        sustainability["average_stay"]
        / sustainability["average_stay"].max()
    )

    # Weighted prototype pressure score
    sustainability["pressure_score"] = (
        0.6 * sustainability["activity_pressure"]
        + 0.4 * sustainability["stay_pressure"]
    ) * 100

    sustainability["pressure_score"] = (
        sustainability["pressure_score"].round(1)
    )

    # Categorize pressure
    sustainability["pressure_level"] = (
        sustainability["pressure_score"]
        .apply(pressure_category)
    )

    return sustainability
