import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_processing import load_tourism_data
from src.flow_analysis import (
    calculate_tourism_flows,
    calculate_destination_activity,
    get_top_destination,
    get_destination_coordinates,
    get_origin_coordinates
)
from src.segmentation import (
    calculate_visitor_segments,
    calculate_activity_profile,
    calculate_segment_destination
)
from src.sustainability import calculate_sustainability_pressure
from src.hospitality import calculate_hospitality_opportunities
from src.recommendations import generate_destination_recommendations
from src.agent import tourflow_agent


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="TourFlow AI",
    page_icon="🌍",
    layout="wide"
)


# =========================================================
# CUSTOM STYLE
# =========================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .metric-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        text-align: center;
    }

    .metric-title {
        color: #8b949e;
        font-size: 14px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
    }

    .insight-box {
        background-color: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-top: 15px;
        line-height: 1.7;
    }

    .agent-box {
        background-color: #161b22;
        padding: 24px;
        border-radius: 14px;
        border: 1px solid #30363d;
        margin-top: 15px;
        line-height: 1.8;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

DATA_PATH = "data/tourism_traces.csv"

df = load_tourism_data(DATA_PATH)


# =========================================================
# ANALYTICS PIPELINE
# =========================================================

flows = calculate_tourism_flows(df)

destination_activity = calculate_destination_activity(df)

top_destination = get_top_destination(df)

destination_coordinates = get_destination_coordinates(df)

origin_coordinates = get_origin_coordinates(df)

visitor_segments = calculate_visitor_segments(df)

activity_profile = calculate_activity_profile(df)

segment_destination = calculate_segment_destination(df)

sustainability = calculate_sustainability_pressure(df)

hospitality = calculate_hospitality_opportunities(df)

recommendations = generate_destination_recommendations(
    sustainability,
    hospitality
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🌍 TourFlow AI")

st.sidebar.caption(
    "From Tourism Flows to Sustainable Destination Management"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Tourism Flows",
        "Tourism Segmentation",
        "Destination Insight",
        "🤖 AI Decision Agent",
        "Sustainability",
        "Hospitality Opportunities",
        "Destination Recommendations",
        "Research Method"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Research Prototype\n\n"
    "Synthetic / Demo Dataset"
)


# =========================================================
# HEADER
# =========================================================

st.title("🌍 TourFlow AI")

st.caption(
    "From Tourism Flows to Sustainable Destination Management"
)

st.markdown("---")


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.subheader("Research Dashboard")

    st.caption(
        "Integrated tourism-flow, segmentation, sustainability "
        "and hospitality analysis."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Tourism Activity
                </div>
                <div class="metric-value">
                    {len(df)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Active Destinations
                </div>
                <div class="metric-value">
                    {df["destination"].nunique()}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Major Tourism Destination
                </div>
                <div class="metric-value">
                    {top_destination}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        avg_stay = df["stay_days"].mean()

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Average Stay
                </div>
                <div class="metric-value">
                    {avg_stay:.1f} days
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Destination Activity")

        fig = px.bar(
            destination_activity,
            x="destination",
            y="tourism_records",
            title="Tourism Records by Destination"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Tourism Segments")

        fig = px.pie(
            visitor_segments,
            names="visitor_segment",
            values="visitors",
            title="Visitor Segment Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Tourism Flow Map")

    fig_map = px.scatter_map(
        destination_coordinates,
        lat="latitude",
        lon="longitude",
        hover_name="destination",
        zoom=4,
        height=500
    )

    fig_map.update_traces(
        marker=dict(size=14)
    )

    for _, origin_row in origin_coordinates.iterrows():

        for _, destination_row in destination_coordinates.iterrows():

            fig_map.add_trace(
                dict(
                    type="scattermap",
                    lat=[
                        origin_row["latitude"],
                        destination_row["latitude"]
                    ],
                    lon=[
                        origin_row["longitude"],
                        destination_row["longitude"]
                    ],
                    mode="lines",
                    line=dict(width=1),
                    hoverinfo="skip",
                    showlegend=False
                )
            )

    st.plotly_chart(
        fig_map,
        use_container_width=True
    )

    st.subheader("Tourism Trace Data")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Research Prototype — Synthetic/Demo Dataset. "
        "Values shown here demonstrate the analytical workflow "
        "and do not represent validated real-world tourism statistics."
    )


# =========================================================
# TOURISM FLOWS
# =========================================================

elif page == "Tourism Flows":

    st.header("Tourism Flow Analysis")

    st.write(
        "The flow-analysis module identifies movement patterns "
        "between tourism origins and destinations."
    )

    st.subheader("Major Tourism Flows")

    st.dataframe(
        flows,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Top Tourism Flows")

    top_flows = flows.head(10)

    fig = px.bar(
        top_flows,
        x="trips",
        y="destination",
        color="origin",
        orientation="h",
        title="Major Origin-Destination Tourism Flows"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Tourism Trace Data")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TOURISM SEGMENTATION
# =========================================================

elif page == "Tourism Segmentation":

    st.header("Tourism Segmentation")

    st.write(
        "Visitor records are segmented using observed visitor "
        "types and activity profiles."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Visitor Segments")

        fig = px.pie(
            visitor_segments,
            names="visitor_segment",
            values="visitors",
            title="Visitor Segment Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Activity Profile")

        fig = px.bar(
            activity_profile,
            x="activity_type",
            y="records",
            title="Tourism Activity Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Segments Across Destinations")

    st.dataframe(
        segment_destination,
        use_container_width=True
    )


# =========================================================
# DESTINATION INSIGHT
# =========================================================

elif page == "Destination Insight":

    st.header("Destination Insight")

    destination = st.selectbox(
        "Select a destination",
        sorted(df["destination"].unique())
    )

    destination_df = df[
        df["destination"] == destination
    ]

    destination_sustainability = sustainability[
        sustainability["destination"] == destination
    ].iloc[0]

    destination_hospitality = hospitality[
        hospitality["destination"] == destination
    ].iloc[0]

    records = len(destination_df)

    average_stay = destination_df["stay_days"].mean()

    top_segment = (
        destination_df["visitor_type"]
        .value_counts()
        .idxmax()
    )

    top_activity = (
        destination_df["activity_type"]
        .value_counts()
        .idxmax()
    )

    pressure_score = destination_sustainability[
        "pressure_score"
    ]

    pressure_level = destination_sustainability[
        "pressure_level"
    ]

    opportunity = destination_hospitality[
        "opportunity"
    ]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Tourism Records", records)

    with col2:
        st.metric(
            "Average Stay",
            f"{average_stay:.1f} days"
        )

    with col3:
        st.metric(
            "Top Visitor Segment",
            top_segment
        )

    with col4:
        st.metric(
            "Pressure Score",
            pressure_score
        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Visitor Profile")

        profile = (
            destination_df["visitor_type"]
            .value_counts()
            .reset_index()
        )

        profile.columns = [
            "visitor_type",
            "visitors"
        ]

        fig = px.bar(
            profile,
            x="visitor_type",
            y="visitors",
            title=f"Visitor Segments — {destination}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Destination Indicators")

        st.write(
            f"**Dominant Activity:** {top_activity}"
        )

        st.write(
            f"**Hospitality Opportunity:** {opportunity}"
        )

        st.write(
            f"**Sustainability Status:** {pressure_level}"
        )

        st.write(
            f"**Prototype Pressure Score:** {pressure_score}"
        )

    recommendation_row = recommendations[
        recommendations["destination"] == destination
    ].iloc[0]

    st.subheader("Management Recommendation")

    st.markdown(
        f"""
        <div class="insight-box">
        {recommendation_row["management_recommendation"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "These insights are generated from the synthetic "
        "research prototype dataset."
    )


# =========================================================
# AI DECISION AGENT
# =========================================================

elif page == "🤖 AI Decision Agent":

    st.header("🤖 TourFlow AI Decision Agent")

    st.write(
        "The TourFlow Orchestrator integrates outputs from "
        "tourism-flow analysis, visitor segmentation, "
        "sustainability assessment and hospitality analysis "
        "to generate a destination-management insight."
    )

    st.markdown("---")

    destination = st.selectbox(
        "Select a destination for AI analysis",
        sorted(df["destination"].unique())
    )

    destination_df = df[
        df["destination"] == destination
    ]

    destination_sustainability = sustainability[
        sustainability["destination"] == destination
    ].iloc[0]

    destination_hospitality = hospitality[
        hospitality["destination"] == destination
    ].iloc[0]

    records = len(destination_df)

    average_stay = destination_df["stay_days"].mean()

    top_segment = (
        destination_df["visitor_type"]
        .value_counts()
        .idxmax()
    )

    top_activity = (
        destination_df["activity_type"]
        .value_counts()
        .idxmax()
    )

    pressure_score = destination_sustainability[
        "pressure_score"
    ]

    pressure_level = destination_sustainability[
        "pressure_level"
    ]

    opportunity = destination_hospitality[
        "opportunity"
    ]

    # -----------------------------------------------------
    # AGENT INPUTS
    # -----------------------------------------------------

    st.subheader("Agent Inputs")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Tourism Records",
            records
        )

    with col2:
        st.metric(
            "Visitor Segment",
            top_segment
        )

    with col3:
        st.metric(
            "Pressure",
            pressure_level
        )

    with col4:
        st.metric(
            "Hospitality",
            opportunity
        )

    st.markdown("---")

    # -----------------------------------------------------
    # FLOW ANALYSIS
    # -----------------------------------------------------

    st.subheader("Major Tourism Origins")

    destination_flows = (
        destination_df
        .groupby("origin")
        .size()
        .reset_index(name="trips")
        .sort_values(
            "trips",
            ascending=False
        )
    )

    st.dataframe(
        destination_flows,
        use_container_width=True,
        hide_index=True
    )

    flow_chart = px.bar(
        destination_flows,
        x="origin",
        y="trips",
        title=f"Origin Markets — {destination}"
    )

    st.plotly_chart(
        flow_chart,
        use_container_width=True
    )

    st.markdown("---")

    # -----------------------------------------------------
    # AGENT REASONING PIPELINE
    # -----------------------------------------------------

    st.subheader("Agent Reasoning Pipeline")

    st.markdown(
        """
        **Tourism Flows**
        ↓  
        **Visitor Segmentation**
        ↓  
        **Sustainability Analysis**
        ↓  
        **Hospitality Opportunity**
        ↓  
        **Destination Recommendation**
        """
    )

    st.markdown("---")

    # -----------------------------------------------------
    # RUN AGENT
    # -----------------------------------------------------

    if st.button(
        "🤖 Generate AI Destination Insight",
        use_container_width=True
    ):

        with st.spinner(
            "TourFlow Agent is analyzing the destination..."
        ):

            agent_result = tourflow_agent(
                df=df,
                destination=destination,
                tourism_records=records,
                average_stay=round(
                    average_stay,
                    1
                ),
                top_segment=top_segment,
                top_activity=top_activity,
                pressure_score=pressure_score,
                pressure_level=pressure_level,
                hospitality_opportunity=opportunity
            )

        st.success(
            "TourFlow Agent analysis completed."
        )

        st.subheader(
            f"AI Destination Insight — {destination}"
        )

        st.markdown(
            f"""
            <div class="agent-box">

            <strong>🤖 TourFlow Orchestrator</strong>

            <br><br>

            {agent_result["final_insight"]}

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # -------------------------------------------------
        # FLOW INSIGHT
        # -------------------------------------------------

        st.subheader("🔎 Flow Insight")

        st.write(
            agent_result["flow_insight"]
        )

        st.markdown("---")

        # -------------------------------------------------
        # DECISION COMPONENTS
        # -------------------------------------------------

        st.subheader("Decision Components")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"""
                **Tourism Flow**

                {records} tourism records were observed
                for {destination}.

                **Visitor Segment**

                The dominant segment is
                **{top_segment}**.

                **Activity**

                The dominant activity is
                **{top_activity}**.
                """
            )

        with col2:

            st.markdown(
                f"""
                **Sustainability**

                Pressure score: **{pressure_score}**

                Pressure level: **{pressure_level}**

                **Hospitality Opportunity**

                **{opportunity}**
                """
            )

        st.markdown("---")

        st.subheader("🧠 Integrated Research Interpretation")

        st.write(
            agent_result["final_insight"]
        )

        st.info(
            "Prototype note: the current TourFlow Agent is a "
            "local orchestration/reasoning layer that integrates "
            "multiple analytical modules. An external LLM can "
            "later be connected for advanced natural-language "
            "reasoning."
        )

    else:

        st.info(
            "Select a destination and click "
            "'Generate AI Destination Insight' to run the agent."
        )


# =========================================================
# SUSTAINABILITY
# =========================================================

elif page == "Sustainability":

    st.header("Sustainability Analysis")

    st.write(
        "TourFlow estimates prototype tourism pressure using "
        "tourism activity, average stay and adventure activity."
    )

    st.subheader("Destination Sustainability Indicators")

    st.dataframe(
        sustainability,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Tourism Pressure Scores")

    fig = px.bar(
        sustainability,
        x="destination",
        y="pressure_score",
        color="pressure_level",
        title="Prototype Sustainability Pressure"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    highest_pressure = sustainability.loc[
        sustainability["pressure_score"].idxmax()
    ]

    st.warning(
        f"Highest prototype pressure is observed for "
        f"{highest_pressure['destination']} "
        f"with a score of "
        f"{highest_pressure['pressure_score']}."
    )

    st.info(
        "The sustainability score is a prototype indicator "
        "developed for this research demonstration. It is "
        "not a validated environmental carrying-capacity metric."
    )


# =========================================================
# HOSPITALITY OPPORTUNITIES
# =========================================================

elif page == "Hospitality Opportunities":

    st.header("Hospitality Opportunities")

    st.write(
        "Destination-level visitor profiles are used to identify "
        "potential hospitality and tourism-service opportunities."
    )

    st.subheader("Destination Opportunities")

    display_hospitality = hospitality.copy()

    display_hospitality["average_stay"] = (
        display_hospitality["average_stay"].round(1)
    )

    st.dataframe(
        display_hospitality,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Opportunity Distribution")

    opportunity_counts = (
        hospitality["opportunity"]
        .value_counts()
        .reset_index()
    )

    opportunity_counts.columns = [
        "opportunity",
        "destinations"
    ]

    fig = px.bar(
        opportunity_counts,
        x="opportunity",
        y="destinations",
        title="Hospitality Opportunity Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# DESTINATION RECOMMENDATIONS
# =========================================================

elif page == "Destination Recommendations":

    st.header("Destination Management Recommendations")

    st.write(
        "Recommendations are generated by combining "
        "sustainability pressure with hospitality opportunities."
    )

    for _, row in recommendations.iterrows():

        with st.expander(
            f"🌍 {row['destination']} — "
            f"{row['pressure_level']} Pressure"
        ):

            st.write(
                f"**Pressure Score:** "
                f"{row['pressure_score']}"
            )

            st.write(
                f"**Hospitality Opportunity:** "
                f"{row['opportunity']}"
            )

            st.write(
                f"**Recommendation:** "
                f"{row['management_recommendation']}"
            )


# =========================================================
# RESEARCH METHOD
# =========================================================

elif page == "Research Method":

    st.header("Research Method")

    st.write(
        "TourFlow AI follows a modular computational tourism "
        "research pipeline."
    )

    st.markdown("---")

    st.subheader("Research Pipeline")

    pipeline = [
        "1. Digital Tourism Data",
        "2. Data Cleaning",
        "3. Geographic / Flow Analysis",
        "4. Tourism Flow Detection",
        "5. Visitor / Destination Segmentation",
        "6. Sustainability Analysis",
        "7. Hospitality Opportunity Analysis",
        "8. AI-Orchestrated Recommendations"
    ]

    for step in pipeline:
        st.write(step)

    st.markdown("---")

    st.subheader("Module Architecture")

    method_data = pd.DataFrame(
        {
            "Module": [
                "Data Processing",
                "Flow Analysis",
                "Segmentation",
                "Sustainability",
                "Hospitality",
                "Recommendations",
                "AI Agent"
            ],
            "Purpose": [
                "Clean and prepare tourism trace data",
                "Identify tourism movement patterns",
                "Identify visitor segments and activities",
                "Estimate prototype tourism pressure",
                "Identify hospitality opportunities",
                "Generate destination-management actions",
                "Integrate analytical outputs into a decision insight"
            ]
        }
    )

    st.dataframe(
        method_data,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("Technology Stack")

    st.write(
        "Python • Pandas • NumPy • Scikit-learn • "
        "Plotly • Streamlit • GeoPandas"
    )

    st.subheader("Research Prototype Status")

    st.info(
        "The current dataset is synthetic/demo data. "
        "The prototype demonstrates the analytical architecture "
        "and can later be evaluated using real-world digital "
        "tourism data."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "TourFlow AI — Research Prototype | "
    "From Tourism Flows to Sustainable Destination Management"
)
