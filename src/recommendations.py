def generate_recommendation(pressure_score, opportunity):
    """
    Generate a prototype destination-management recommendation
    based on sustainability pressure and hospitality opportunity.
    """

    if pressure_score >= 75:
        return (
            "High tourism pressure detected. "
            "Consider visitor-capacity monitoring, "
            "seasonal flow management, and sustainable "
            "accommodation planning."
        )

    elif pressure_score >= 50:
        return (
            f"Moderate tourism pressure. Expand "
            f"{opportunity.lower()} while monitoring "
            "visitor concentration and destination capacity."
        )

    else:
        return (
            f"Lower tourism pressure. Promote "
            f"{opportunity.lower()} to diversify tourism "
            "activity and support local hospitality."
        )


def generate_destination_recommendations(
    sustainability,
    hospitality
):
    """
    Combine sustainability indicators and hospitality
    opportunities to generate destination recommendations.
    """

    recommendations = sustainability.merge(
        hospitality[["destination", "opportunity"]],
        on="destination",
        how="left"
    )

    recommendations["management_recommendation"] = (
        recommendations.apply(
            lambda row: generate_recommendation(
                row["pressure_score"],
                row["opportunity"]
            ),
            axis=1
        )
    )

    return recommendations
