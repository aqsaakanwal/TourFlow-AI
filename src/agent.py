import pandas as pd


# ============================================================
# 1. FLOW ANALYSIS AGENT
# ============================================================

def flow_analysis_agent(df, destination):
    """
    Analyze origin-destination tourism movement
    for a selected destination.
    """

    destination_df = df[
        df["destination"] == destination
    ]

    flow_data = (
        destination_df
        .groupby("origin")
        .size()
        .reset_index(name="trips")
        .sort_values(
            "trips",
            ascending=False
        )
    )

    if flow_data.empty:

        return {
            "flow_data": flow_data,
            "top_origin": "Unknown",
            "top_trips": 0,
            "insight": (
                "No tourism flow data is available "
                f"for {destination}."
            )
        }

    top_origin = flow_data.iloc[0]["origin"]

    top_trips = int(
        flow_data.iloc[0]["trips"]
    )

    insight = (
        f"{top_origin} is the leading origin market "
        f"for {destination}, with {top_trips} observed "
        "tourism trips in the prototype dataset."
    )

    return {
        "flow_data": flow_data,
        "top_origin": top_origin,
        "top_trips": top_trips,
        "insight": insight
    }


# ============================================================
# 2. VISITOR SEGMENTATION AGENT
# ============================================================

def segmentation_agent(df, destination):
    """
    Identify dominant visitor segment and activity
    for a selected destination.
    """

    destination_df = df[
        df["destination"] == destination
    ]

    if destination_df.empty:

        return {
            "top_segment": "Unknown",
            "top_activity": "Unknown",
            "segment_counts": pd.Series(
                dtype="int64"
            ),
            "activity_counts": pd.Series(
                dtype="int64"
            ),
            "insight": (
                "No visitor segmentation data "
                f"is available for {destination}."
            )
        }

    segment_counts = (
        destination_df["visitor_type"]
        .value_counts()
    )

    activity_counts = (
        destination_df["activity_type"]
        .value_counts()
    )

    top_segment = segment_counts.idxmax()

    top_activity = activity_counts.idxmax()

    segment_percentage = (
        segment_counts.iloc[0]
        / len(destination_df)
    ) * 100

    insight = (
        f"The dominant visitor segment in {destination} "
        f"is {top_segment}, representing approximately "
        f"{segment_percentage:.1f}% of observed records. "
        f"The dominant activity is {top_activity}."
    )

    return {
        "top_segment": top_segment,
        "top_activity": top_activity,
        "segment_counts": segment_counts,
        "activity_counts": activity_counts,
        "insight": insight
    }


# ============================================================
# 3. SUSTAINABILITY AGENT
# ============================================================

def sustainability_agent(
    pressure_score,
    pressure_level
):
    """
    Interpret the prototype sustainability pressure
    indicator and identify a management response.
    """

    if pressure_level == "High":

        action = (
            "visitor-capacity monitoring, seasonal flow "
            "management, and sustainable accommodation planning"
        )

        interpretation = (
            "The destination shows relatively high "
            "tourism pressure within the prototype model."
        )

    elif pressure_level == "Moderate":

        action = (
            "monitoring visitor concentration and destination "
            "capacity while supporting controlled tourism growth"
        )

        interpretation = (
            "The destination shows moderate tourism pressure "
            "and may benefit from balanced tourism management."
        )

    else:

        action = (
            "responsible tourism promotion and diversification "
            "of visitor activities"
        )

        interpretation = (
            "The destination shows comparatively lower "
            "tourism pressure within the prototype model."
        )

    insight = (
        f"{interpretation} The prototype pressure score "
        f"is {pressure_score:.1f}, classified as "
        f"{pressure_level} pressure."
    )

    return {
        "pressure_score": pressure_score,
        "pressure_level": pressure_level,
        "interpretation": interpretation,
        "recommended_action": action,
        "insight": insight
    }


# ============================================================
# 4. HOSPITALITY OPPORTUNITY AGENT
# ============================================================

def hospitality_agent(df, destination):
    """
    Infer a potential hospitality opportunity
    from the dominant visitor profile.
    """

    destination_df = df[
        df["destination"] == destination
    ]

    if destination_df.empty:

        return {
            "opportunity": "Unknown",
            "dominant_segment": "Unknown",
            "insight": (
                "No hospitality data is available "
                f"for {destination}."
            )
        }

    visitor_counts = (
        destination_df["visitor_type"]
        .value_counts()
    )

    top_segment = visitor_counts.idxmax()

    if top_segment == "Adventure":

        opportunity = (
            "Adventure Tourism Services"
        )

        rationale = (
            "The visitor profile suggests demand for "
            "adventure-oriented tourism services."
        )

    elif top_segment == "Nature":

        opportunity = (
            "Eco / Nature Hospitality"
        )

        rationale = (
            "The visitor profile suggests potential for "
            "eco-oriented accommodation and nature-based services."
        )

    elif top_segment == "Cultural":

        opportunity = (
            "Cultural Tourism Services"
        )

        rationale = (
            "The visitor profile suggests opportunities "
            "for culturally oriented tourism services."
        )

    else:

        opportunity = (
            "Diversified Tourism Services"
        )

        rationale = (
            "The visitor profile suggests potential for "
            "diversified tourism and hospitality services."
        )

    insight = (
        f"{rationale} The dominant observed segment "
        f"is {top_segment}."
    )

    return {
        "opportunity": opportunity,
        "dominant_segment": top_segment,
        "rationale": rationale,
        "insight": insight
    }


# ============================================================
# 5. RECOMMENDATION AGENT
# ============================================================

def recommendation_agent(
    pressure_level,
    sustainability_action,
    hospitality_opportunity,
    top_segment,
    top_activity
):
    """
    Combine sustainability and hospitality signals
    into a destination-management recommendation.
    """

    if pressure_level == "High":

        recommendation = (
            f"Prioritize visitor-capacity monitoring and "
            f"{sustainability_action}. At the same time, "
            f"support {hospitality_opportunity.lower()} "
            f"that aligns with the dominant {top_segment.lower()} "
            f"visitor profile and {top_activity.lower()} activity."
        )

    elif pressure_level == "Moderate":

        recommendation = (
            f"Support controlled tourism growth through "
            f"{hospitality_opportunity.lower()} while "
            f"monitoring visitor concentration and destination "
            f"capacity. Planning should remain aligned with "
            f"{top_segment.lower()} visitors and "
            f"{top_activity.lower()} activity."
        )

    else:

        recommendation = (
            f"Promote responsible tourism and "
            f"{hospitality_opportunity.lower()} to diversify "
            f"destination activity. The current profile suggests "
            f"an opportunity to strengthen services for "
            f"{top_segment.lower()} visitors interested in "
            f"{top_activity.lower()}."
        )

    return recommendation


# ============================================================
# 6. TOURFLOW ORCHESTRATOR AGENT
# ============================================================

def tourflow_agent(
    df,
    destination,
    tourism_records,
    average_stay,
    top_segment,
    top_activity,
    pressure_score,
    pressure_level,
    hospitality_opportunity
):
    """
    TourFlow Orchestrator.

    Coordinates specialized analytical agents and
    integrates their outputs into one destination-level
    decision-support insight.
    """

    # --------------------------------------------------------
    # RUN SPECIALIZED AGENTS
    # --------------------------------------------------------

    flow_result = flow_analysis_agent(
        df,
        destination
    )

    segmentation_result = segmentation_agent(
        df,
        destination
    )

    sustainability_result = sustainability_agent(
        pressure_score,
        pressure_level
    )

    hospitality_result = hospitality_agent(
        df,
        destination
    )

    # --------------------------------------------------------
    # USE AGENT RESULTS
    # --------------------------------------------------------

    final_segment = (
        segmentation_result["top_segment"]
    )

    final_activity = (
        segmentation_result["top_activity"]
    )

    final_opportunity = (
        hospitality_result["opportunity"]
    )

    # --------------------------------------------------------
    # GENERATE RECOMMENDATION
    # --------------------------------------------------------

    recommendation = recommendation_agent(
        pressure_level=pressure_level,
        sustainability_action=(
            sustainability_result[
                "recommended_action"
            ]
        ),
        hospitality_opportunity=final_opportunity,
        top_segment=final_segment,
        top_activity=final_activity
    )

    # --------------------------------------------------------
    # BUILD INTEGRATED INSIGHT
    # --------------------------------------------------------

    final_insight = (
        f"TourFlow AI analyzed {tourism_records} "
        f"tourism records for {destination}. "
        f"The average observed stay is "
        f"{average_stay:.1f} days. "
        f"{flow_result['insight']} "
        f"{segmentation_result['insight']} "
        f"{sustainability_result['insight']} "
        f"{hospitality_result['insight']} "
        f"Overall, the prototype suggests: "
        f"{recommendation}"
    )

    # --------------------------------------------------------
    # RETURN COMPLETE AGENT OUTPUT
    # --------------------------------------------------------

    return {

        # Flow Agent
        "flow_data": (
            flow_result["flow_data"]
        ),

        "flow_insight": (
            flow_result["insight"]
        ),

        "top_origin": (
            flow_result["top_origin"]
        ),

        # Segmentation Agent
        "segment_insight": (
            segmentation_result["insight"]
        ),

        "top_segment": (
            final_segment
        ),

        "top_activity": (
            final_activity
        ),

        # Sustainability Agent
        "sustainability_insight": (
            sustainability_result["insight"]
        ),

        "pressure_score": (
            sustainability_result[
                "pressure_score"
            ]
        ),

        "pressure_level": (
            sustainability_result[
                "pressure_level"
            ]
        ),

        # Hospitality Agent
        "hospitality_insight": (
            hospitality_result["insight"]
        ),

        "hospitality_opportunity": (
            final_opportunity
        ),

        # Recommendation Agent
        "recommendation": (
            recommendation
        ),

        # Orchestrator
        "final_insight": (
            final_insight
        )
    }
