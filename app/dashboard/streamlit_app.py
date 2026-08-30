import streamlit as st
import pandas as pd
import plotly.express as px

from app.graph.workflow import build_graph


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AEGIS | Enterprise Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CLEAN ENTERPRISE STYLING
# ============================================================

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background-color: #F5F7FB;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}


/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: #E5E7EB;
}


/* Headings */

h1, h2, h3 {
    color: #111827;
}


/* Cards */

.enterprise-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
}


/* KPI cards */

.kpi-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 20px;
    min-height: 125px;
}

.kpi-label {
    color: #6B7280;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.kpi-value {
    color: #111827;
    font-size: 1.8rem;
    font-weight: 700;
    margin-top: 8px;
}

.kpi-description {
    color: #6B7280;
    font-size: 0.82rem;
    margin-top: 6px;
}


/* Agent cards */

.agent-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-left: 4px solid #2563EB;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
}

.agent-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #111827;
}

.agent-status {
    color: #15803D;
    font-size: 0.8rem;
    font-weight: 700;
}

.agent-description {
    color: #6B7280;
    font-size: 0.85rem;
    margin-top: 8px;
}


/* Section spacing */

.section-space {
    margin-top: 28px;
}


/* Buttons */

.stButton > button {
    height: 48px;
    border-radius: 10px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛡️ AEGIS")

    st.caption("ENTERPRISE INTELLIGENCE PLATFORM")

    st.divider()

    st.markdown("### PLATFORM")

    st.write("🏠 Command Center")
    st.write("🤖 Agent Operations")
    st.write("📊 Data Intelligence")
    st.write("📚 Evidence & Sources")

    st.divider()

    st.markdown("### SYSTEM STATUS")

    st.success("● Operational")

    st.caption("Multi-Agent Orchestration")
    st.caption("SQL Intelligence")
    st.caption("Internal Knowledge Retrieval")
    st.caption("External Market Research")

    st.divider()

    st.caption("AEGIS v1.0.0")


# ============================================================
# HEADER
# ============================================================

st.title("Enterprise Intelligence Command Center")

st.caption(
    "Analyze enterprise data, internal knowledge, and external "
    "market intelligence using coordinated AI agents."
)

st.divider()


# ============================================================
# QUERY WORKSPACE
# ============================================================

st.subheader("Intelligence Workspace")

query = st.text_area(
    "Enterprise Question",
    placeholder=(
        "Example: Why did enterprise revenue decline in Q2? "
        "Analyze revenue data, internal company documents, "
        "and external market conditions."
    ),
    height=130,
)

run_analysis = st.button(
    "Run Intelligence Analysis",
    type="primary",
    use_container_width=True,
)


# ============================================================
# EMPTY STATE
# ============================================================

if not run_analysis:

    st.divider()

    st.subheader("Platform Overview")

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("ACTIVE AGENTS", "5", "Planner and specialist agents"),
        ("DATA SYSTEMS", "3", "SQL, RAG, and Research"),
        ("ORCHESTRATION", "LangGraph", "Coordinated workflow"),
        ("SYSTEM STATUS", "READY", "Waiting for a question"),
    ]

    for column, metric in zip(
        [c1, c2, c3, c4],
        metrics,
    ):

        with column:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{metric[0]}</div>
                    <div class="kpi-value">{metric[1]}</div>
                    <div class="kpi-description">{metric[2]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


    st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)

    left, right = st.columns(2)


    with left:

        st.subheader("Agent Workflow")

        workflow_steps = [
            "🧠 Planning Agent — Understands the enterprise question",
            "🗄️ SQL Agent — Analyzes structured enterprise data",
            "📄 RAG Agent — Searches internal documents",
            "🌐 Research Agent — Investigates external conditions",
            "🎯 Synthesizer — Produces executive intelligence",
        ]

        for step in workflow_steps:
            st.info(step)


    with right:

        st.subheader("What You Can Ask")

        examples = [
            "What is the total revenue by region?",
            "Which customer segment has the highest sales?",
            "Why did revenue decline in Q2?",
            "What do internal documents say about customer churn?",
            "What external market conditions could affect revenue?",
        ]

        for example in examples:
            st.write(f"• {example}")


    st.stop()


# ============================================================
# VALIDATION
# ============================================================

if not query.strip():

    st.warning("Please enter an enterprise analysis question.")

    st.stop()


# ============================================================
# RUN ANALYSIS
# ============================================================

st.divider()

st.subheader("Live Analysis")

progress = st.progress(0)

status = st.empty()

try:

    status.info("🧠 Planning enterprise analysis...")

    progress.progress(20)

    graph = build_graph()

    status.info("🤖 Executing specialized intelligence agents...")

    progress.progress(50)

    result = graph.invoke(
        {
            "query": query
        }
    )

    status.info("🎯 Synthesizing enterprise evidence...")

    progress.progress(90)

    progress.progress(100)

    status.success("Analysis completed successfully.")

except Exception as error:

    status.error("Analysis failed.")

    st.exception(error)

    st.stop()


# ============================================================
# EXTRACT RESULTS
# ============================================================

execution_plan = result.get("execution_plan", [])

agent_results = result.get("agent_results", {})

final_answer = result.get("final_answer", "")


sql_results = [
    value
    for value in agent_results.values()
    if value.get("agent") == "sql"
]


total_sources = sum(
    len(value.get("sources", []))
    for value in agent_results.values()
)


completed_agents = len(
    [
        value
        for value in agent_results.values()
        if value.get("status") == "completed"
    ]
)


data_records = sum(
    value.get("row_count", 0)
    for value in sql_results
)


# ============================================================
# KPI OVERVIEW
# ============================================================

st.divider()

st.subheader("Executive Overview")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Tasks Executed",
    len(execution_plan),
)

m2.metric(
    "Agents Completed",
    completed_agents,
)

m3.metric(
    "Data Records",
    data_records,
)

m4.metric(
    "Evidence Sources",
    total_sources,
)


# ============================================================
# MAIN TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Executive Report",
        "🤖 Agent Operations",
        "🗄️ Data Intelligence",
        "📚 Evidence & Sources",
    ]
)


# ============================================================
# TAB 1 — EXECUTIVE REPORT
# ============================================================

with tab1:

    st.subheader("Executive Decision Report")

    if final_answer:

        st.markdown(final_answer)

    else:

        st.warning(
            "No executive synthesis was returned."
        )


# ============================================================
# TAB 2 — AGENT OPERATIONS
# ============================================================

with tab2:

    st.subheader("Agent Execution")

    if not execution_plan:
        st.info("No agent tasks were executed.")

    for task in execution_plan:

        task_id = task.get("id", "Unknown Task")

        agent_name = task.get(
            "agent",
            "unknown",
        ).upper()

        task_description = task.get(
            "description",
            "No task description available.",
        )

        agent_result = agent_results.get(
            task_id,
            {},
        )

        agent_status = agent_result.get(
            "status",
            "unknown",
        )

        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(
                f"### {agent_name} AGENT"
            )

        with col2:

            if agent_status == "completed":
                st.success("COMPLETED")

            elif agent_status == "failed":
                st.error("FAILED")

            else:
                st.warning(
                    agent_status.upper()
                )

        st.caption("TASK")

        st.write(
            task_description
        )

        if agent_status == "completed":

            if task.get("agent") == "sql":

                row_count = agent_result.get(
                    "row_count",
                    0,
                )

                st.success(
                    f"Structured analysis completed successfully. "
                    f"{row_count} records returned."
                )

            elif task.get("agent") == "research":

                source_count = agent_result.get(
                    "source_count",
                    0,
                )

                st.success(
                    f"External research completed successfully. "
                    f"{source_count} sources analyzed."
                )

            elif task.get("agent") == "rag":

                st.success(
                    "Internal knowledge retrieval completed successfully."
                )

            else:

                st.success(
                    "Agent completed successfully."
                )

        else:

            error_message = agent_result.get(
                "error",
                "No additional error details available.",
            )

            st.error(
                f"Agent execution issue: {error_message}"
            )

        st.divider()


# ============================================================
# TAB 3 — DATA INTELLIGENCE
# ============================================================

# ============================================================

with tab3:

    if not sql_results:

        st.info(
            "No structured database analysis was required "
            "for this question."
        )

    for sql_result in sql_results:

        rows = sql_result.get(
            "rows",
            [],
        )

        if rows:

            df = pd.DataFrame(rows)

            st.subheader(
                "Structured Enterprise Evidence"
            )

            chart_col, table_col = st.columns(
                [1.2, 1]
            )


            numeric_columns = df.select_dtypes(
                include="number"
            ).columns.tolist()

            categorical_columns = df.select_dtypes(
                exclude="number"
            ).columns.tolist()


            with chart_col:

                if (
                    numeric_columns
                    and categorical_columns
                ):

                    chart = px.bar(
                        df,
                        x=categorical_columns[0],
                        y=numeric_columns[0],
                        title="Enterprise Data Analysis",
                        text_auto=True,
                    )

                    chart.update_layout(
                        height=420,
                    )

                    st.plotly_chart(
                        chart,
                        use_container_width=True,
                    )


            with table_col:

                st.dataframe(
                    df,
                    use_container_width=True,
                    height=420,
                )


        sql_query = sql_result.get(
            "sql",
            "",
        )

        if sql_query:

            with st.expander(
                "View Generated SQL"
            ):

                st.code(
                    sql_query,
                    language="sql",
                )


# ============================================================
# TAB 4 — EVIDENCE AND SOURCES
# ============================================================

with tab4:

    left, right = st.columns(
        [1.2, 1]
    )


    with left:

        st.subheader("Agent Evidence")

        evidence_found = False

        for agent_result in agent_results.values():

            if agent_result.get(
                "agent"
            ) in ["rag", "research"]:

                evidence_found = True

                agent_name = agent_result.get(
                    "agent",
                    "unknown",
                ).upper()

                with st.expander(
                    f"{agent_name} ANALYSIS",
                    expanded=True,
                ):

                    st.markdown(
                        agent_result.get(
                            "analysis",
                            "No analysis returned.",
                        )
                    )


        if not evidence_found:

            st.info(
                "No internal or external evidence "
                "was required for this question."
            )


    with right:

        st.subheader("Sources")

        source_found = False

        for agent_result in agent_results.values():

            sources = agent_result.get(
                "sources",
                [],
            )

            for source in sources:

                source_found = True

                if isinstance(
                    source,
                    dict,
                ):

                    title = source.get(
                        "title",
                        "Source",
                    )

                    url = source.get(
                        "url",
                        "",
                    )

                    if url:

                        st.markdown(
                            f"🔗 [{title}]({url})"
                        )

                    else:

                        st.write(
                            f"📄 {title}"
                        )

                else:

                    st.write(
                        f"📄 {source}"
                    )


        if not source_found:

            st.info(
                "No external sources were used "
                "for this analysis."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AEGIS ENTERPRISE INTELLIGENCE PLATFORM  •  "
    "MULTI-AGENT AI DECISION SYSTEM"
)

