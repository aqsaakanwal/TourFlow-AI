def determine_opportunity(row):
    """
    Identify a prototype hospitality opportunity
    based on visitor segment patterns.
    """

    if row["adventure_visitors"] >= max(
        row["nature_visitors"],
        row["cultural_visitors"]
    ):
        return "Adventure Tourism Services"

    elif row["nature_visitors"] >= row["cultural_visitors"]:
        return "Eco / Nature Hospitality"

    else:
        return "Cultural Tourism Services"


def calculate_hospitality_opportunities(df):
    """
    Analyze destination-level hospitality opportunities.
    """

    hospitality = (
        df.groupby("destination")
        .agg(
            tourism_demand=("visitor_id", "count"),
            average_stay=("stay_days", "mean"),
            adventure_visitors=(
                "visitor_type",
                lambda x: (x == "Adventure").sum()
            ),
            nature_visitors=(
                "visitor_type",
                lambda x: (x == "Nature").sum()
            ),
            cultural_visitors=(
                "visitor_type",
                lambda x: (x == "Cultural").sum()
            )
        )
        .reset_index()
    )

    hospitality["opportunity"] = hospitality.apply(
        determine_opportunity,
        axis=1
    )

    return hospitality
