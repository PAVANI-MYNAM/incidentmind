import re
import streamlit as st

from agent.agent import analyze_incident
from memory.hindsight_client import (
    remember_incident,
    record_incident_outcome,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="IncidentMind - A memory-powered AI Incident Response Engineer",
    page_icon="🧠",
    layout="wide",
)

st.title("IncidentMind - A memory-powered AI Incident Response Engineer")
st.subheader("Every incident makes the next incident easier to solve")


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        opacity: 0.75;
        margin-bottom: 25px;
    }

    .memory-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 12px;
    }

    .similar-card {
        padding: 20px;
        border-radius: 14px;
        border: 1px solid rgba(80,140,255,0.35);
        background: rgba(80,140,255,0.06);
        margin-bottom: 15px;
    }

    .impact-card {
        padding: 20px;
        border-radius: 14px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 15px;
    }

    .success-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(0,180,100,0.4);
        background: rgba(0,180,100,0.08);
        margin-top: 10px;
    }

    .incident-id {
        font-weight: 700;
        font-size: 17px;
    }

    .small-text {
        font-size: 13px;
        opacity: 0.7;
    }

    .section-label {
        font-size: 14px;
        font-weight: 700;
        opacity: 0.7;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "incident_resolved" not in st.session_state:
    st.session_state.incident_resolved = False

if "learning_complete" not in st.session_state:
    st.session_state.learning_complete = False


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 🧠 IncidentMind")

    st.caption("Memory-powered AI Incident Response")

    st.divider()

    st.markdown("### System")

    st.success("Hindsight Memory: Connected")
    st.success("Groq AI: Connected")

    st.divider()

    st.markdown("### 🧠 Memory Mode")

    memory_mode = st.radio(
        "Choose how IncidentMind should analyze this incident:",
        [
            "With Hindsight Memory",
            "Without Hindsight Memory",
        ],
        index=0,
    )

    use_memory = memory_mode == "With Hindsight Memory"

    if use_memory:
        st.info(
            "Hindsight is enabled. "
            "IncidentMind will use up to 4 relevant historical incidents."
        )
    else:
        st.warning(
            "Hindsight is disabled. "
            "IncidentMind will analyze only the current incident."
        )


# ============================================================
# TOP METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Memory", "Hindsight")

with col2:
    st.metric("AI Engine", "Groq")

with col3:
    st.metric("Workflow", "Incident Response")

with col4:
    st.metric("Learning", "Enabled")


st.divider()


# ============================================================
# INCIDENT INPUT
# ============================================================

st.markdown("## 🚨 New Production Incident")

st.caption(
    "Enter the details of the current production incident. "
    "IncidentMind will search its organizational memory "
    "before generating a diagnosis."
)


# ============================================================
# INCIDENT ID + SEVERITY
# ============================================================

col1, col2 = st.columns([2, 1])

with col1:
    incident_id = st.text_input(
        "Incident ID",
        placeholder="Example: INC-1001",
    )

with col2:
    severity = st.selectbox(
        "Severity",
        [
            "Select severity",
            "critical",
            "high",
            "medium",
            "low",
        ],
        index=0,
    )


# ============================================================
# SERVICE + TIMESTAMP
# ============================================================

col1, col2 = st.columns(2)

with col1:
    service = st.text_input(
        "Affected Service",
        placeholder="Example: payment-api",
    )

with col2:
    timestamp = st.text_input(
        "Incident Time",
        placeholder="Example: 2026-09-28T14:30:00",
    )


# ============================================================
# SYMPTOMS
# ============================================================

symptoms_text = st.text_area("Symptoms", placeholder=("Example:HTTP 503 errors"))


# ============================================================
# RELEVANT LOGS
# ============================================================

logs_text = st.text_area(
    "Relevant Logs", placeholder=("Example:DB connection pool exhausted")
)


# ============================================================
# CONVERT INPUT INTO INCIDENT OBJECT
# ============================================================

symptoms = [line.strip() for line in symptoms_text.split("\n") if line.strip()]

logs = [line.strip() for line in logs_text.split("\n") if line.strip()]


incident = {
    "incident_id": incident_id,
    "service": service,
    "severity": severity,
    "timestamp": timestamp,
    "symptoms": symptoms,
    "logs": logs,
}


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button_text = (
    "🔍 Analyze Incident with Hindsight"
    if use_memory
    else "🔍 Analyze Incident without Memory"
)

if st.button(
    analyze_button_text,
    type="primary",
    use_container_width=True,
):
    if not incident_id.strip():
        st.error("Please enter an Incident ID.")

    elif severity == "Select severity":
        st.error("Please select the incident severity.")

    elif not service.strip():
        st.error("Please enter the affected service.")

    elif not timestamp.strip():
        st.error("Please enter the incident time.")

    elif not symptoms:
        st.error("Please enter at least one symptom.")

    elif not logs:
        st.error("Please enter the relevant logs.")

    else:
        if use_memory:
            spinner_text = "Searching Hindsight memory and analyzing incident..."
        else:
            spinner_text = "Analyzing incident without memory..."

        with st.spinner(spinner_text):
            try:
                result = analyze_incident(
                    incident,
                    use_memory=use_memory,
                )

                if result is None:
                    st.error(
                        "Incident analysis returned no result. "
                        "Please check agent/agent.py."
                    )
                    st.stop()

                if not isinstance(result, dict):
                    st.error(
                        f"Unexpected analysis result type: {type(result).__name__}"
                    )
                    st.stop()

                st.session_state.analysis_result = result
                st.session_state.incident_resolved = False
                st.session_state.learning_complete = False

                st.rerun()

            except Exception as e:
                st.error(
                    f"Incident analysis failed: {type(e).__name__}: {e}"
                )

# ============================================================
# SHOW ANALYSIS
# ============================================================

result = st.session_state.analysis_result


if result is not None:
    st.divider()

    # ========================================================
    # SIMILAR INCIDENTS
    # ========================================================

    st.markdown("## 🔎 Historical Incidents")

    if result.get("memory_enabled", True):

       st.caption(
        "Hindsight is enabled. The most relevant historical incidents are shown below."
    )
    else:
       st.caption(
        "Hindsight is disabled. No historical incidents were provided to the AI."
    )

    # Only consider the 4 most relevant incidents.
    memories = result.get("memories", [])[:4]

    if memories:
        st.success(
            f"Hindsight found {len(memories)} most relevant historical incidents."
        )

        st.caption(
            "These incidents were retrieved from organizational memory "
            "because they contain information relevant to the current incident."
        )

        for index, memory in enumerate(memories):
            st.markdown(
                f"""
                <div class="similar-card">

                <div class="incident-id">
                🧠 Historical Incident {index + 1}
                </div>

                <br>

                {memory}

                </div>
                """,
                unsafe_allow_html=True,
            )

        # ====================================================
        # MEMORY MATCH EXPLANATION
        # ====================================================

        st.markdown("### Why are these incidents similar?")

        match_col1, match_col2, match_col3 = st.columns(3)

        with match_col1:
            st.info(
                f"""
                **Service Match**

                Current service:

                `{incident.get("service")}`

                Hindsight searches historical incidents
                involving the same or related service.
                """
            )

        with match_col2:
            st.info(
                f"""
                **Symptom Match**

                Current symptoms include:

                `{", ".join(symptoms[:2])}`

                Historical memories can contain similar
                failures and symptoms.
                """
            )

        with match_col3:
            st.info(
                """
                **Resolution Evidence**

                Historical incidents contain previous
                root causes, fixes, outcomes and
                engineer feedback.
                """
            )

    else:
        if result.get("memory_enabled", True):
            st.info(
                "No relevant historical memories were found. "
                "This incident can become new organizational knowledge."
            )
        else:
            st.info(
                "Hindsight memory is disabled for this analysis. "
                "The AI is reasoning only from the current incident."
            )

    # ========================================================
    # MEMORY IMPACT
    # ========================================================

    st.divider()

    st.markdown("## 🧠 Memory Impact")

    st.caption(
        "The key difference between a normal AI assistant and "
        "IncidentMind is that IncidentMind can use organizational experience."
    )

    impact_col1, impact_col2 = st.columns(2)

    with impact_col1:
        st.markdown(
            """
            <div class="impact-card">

            <h4>❌ Without Memory</h4>

            <ul>
                <li>Every incident is treated as a new problem.</li>
                <li>AI mainly sees the current symptoms and logs.</li>
                <li>Previous successful fixes are unavailable.</li>
                <li>Past engineer knowledge is lost between incidents.</li>
                <li>The system does not learn from previous outcomes.</li>
            </ul>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with impact_col2:
        st.markdown(
            """
            <div class="impact-card">

            <h4>✅ With Hindsight</h4>

            <ul>
                <li>Similar historical incidents can be recalled.</li>
                <li>Previous root causes become evidence.</li>
                <li>Previously successful resolutions can inform recommendations.</li>
                <li>Engineer feedback becomes organizational knowledge.</li>
                <li>Each resolved incident can improve future responses.</li>
            </ul>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # AI ANALYSIS
    # ========================================================

    st.divider()

    st.markdown("## 🤖 IncidentMind Analysis")

    analysis = result.get("analysis", "")

    # ========================================================
    # LIMIT RECOMMENDED NEXT STEPS TO 3
    # ========================================================

    def limit_recommended_steps(text, max_steps=3):

        pattern = re.compile(
            r"(4\.\s*Recommended Next Steps)(.*?)("
            r"\n\s*5\.\s|\n\s*6\.\s|$)",
            re.IGNORECASE | re.DOTALL,
        )

        match = pattern.search(text)

        if not match:
            return text

        heading = match.group(1)
        section = match.group(2).strip()

        lines = section.splitlines()

        steps = []

        for line in lines:
            stripped = line.strip()

            if not stripped:
                continue

            if re.match(r"^[-*•]\s+", stripped):
                steps.append(stripped)

            elif re.match(r"^\d+[\.\)]\s+", stripped):
                steps.append(stripped)

            elif re.match(
                r"^Step\s+\d+",
                stripped,
                re.IGNORECASE,
            ):
                steps.append(stripped)

        if not steps:
            return text

        limited_steps = steps[:max_steps]

        replacement = f"{heading}\n\n" + "\n".join(limited_steps)

        return text[: match.start()] + replacement + text[match.end() :]

    analysis = limit_recommended_steps(
        analysis,
        max_steps=3,
    )

    st.markdown(analysis)

    # ========================================================
    # ENGINEER APPROVAL
    # ========================================================

    st.divider()

    st.markdown("## 👨‍💻 Engineer Review")

    st.warning(
        "IncidentMind recommends actions. "
        "A human engineer must review and approve the remediation."
    )

    approve = st.checkbox(
        "I reviewed the recommendation and approve the remediation plan."
    )

    if approve:
        st.success("Remediation approved by engineer.")

        st.session_state.incident_resolved = True


# ============================================================
# INCIDENT RESOLUTION / LEARNING
# ============================================================

if st.session_state.incident_resolved:
    st.divider()

    st.markdown("## ✅ Incident Resolution")

    st.caption(
        "After the incident is resolved, record what actually happened. "
        "This becomes new Hindsight memory."
    )

    # ========================================================
    # ACTUAL ROOT CAUSE
    # ========================================================

    actual_root_cause = st.text_area(
        "Actual Root Cause",
        placeholder=("Enter the actual root cause discovered during investigation."),
    )

    # ========================================================
    # ACTUAL RESOLUTION
    # ========================================================

    actual_resolution_text = st.text_area(
        "Actual Resolution",
        placeholder=(
            "Enter what was actually done to resolve "
            "the incident.\n\n"
            "You can enter multiple actions on separate lines."
        ),
        height=120,
    )

    actual_resolution = [
        line.strip() for line in actual_resolution_text.split("\n") if line.strip()
    ]

    # ========================================================
    # OUTCOME
    # ========================================================

    outcome = st.selectbox(
        "Outcome",
        [
            "Select outcome",
            "successful",
            "partially successful",
            "failed",
        ],
        index=0,
    )

    # ========================================================
    # RESOLUTION TIME
    # ========================================================

    resolution_time = st.number_input(
        "Resolution Time (minutes)",
        min_value=1,
        max_value=1440,
        value=None,
        placeholder="Enter resolution time",
    )

    # ========================================================
    # ENGINEER FEEDBACK
    # ========================================================

    engineer_feedback = st.text_area(
        "Engineer Feedback",
        placeholder=(
            "Enter observations, lessons learned, or feedback from the engineer."
        ),
        height=120,
    )

    # ========================================================
    # LEARN BUTTON
    # ========================================================

    if st.button(
        "🧠 Record Outcome & Teach IncidentMind",
        type="primary",
        use_container_width=True,
    ):
        if not actual_root_cause.strip():
            st.error("Please enter the actual root cause.")

        elif not actual_resolution:
            st.error("Please enter the actual resolution.")

        elif outcome == "Select outcome":
            st.error("Please select the incident outcome.")

        elif resolution_time is None:
            st.error("Please enter the resolution time.")

        elif not engineer_feedback.strip():
            st.error("Please enter engineer feedback.")

        else:
            with st.spinner("Storing incident outcome in Hindsight..."):
                try:
                    record_incident_outcome(
                        incident=incident,
                        actual_root_cause=actual_root_cause,
                        actual_resolution=actual_resolution,
                        outcome=outcome,
                        engineer_feedback=engineer_feedback,
                        resolution_time_minutes=resolution_time,
                    )

                    learned_incident = {
                        **incident,
                        "root_cause": actual_root_cause,
                        "resolution": actual_resolution,
                        "resolution_time_minutes": resolution_time,
                        "outcome": outcome,
                        "engineer_feedback": engineer_feedback,
                    }

                    remember_incident(learned_incident)

                    st.session_state.learning_complete = True

                    st.success("IncidentMind learned from this incident!")

                    st.rerun()

                except Exception as e:
                    st.error(f"Learning step failed: {type(e).__name__}: {e}")


# ============================================================
# LEARNING CONFIRMATION
# ============================================================

if st.session_state.learning_complete:
    st.divider()

    st.markdown("## 🧠 What IncidentMind Learned")

    st.markdown(
        """
        <div class="success-card">

        <strong>New organizational memory created.</strong>

        <br><br>

        IncidentMind now remembers:

        <ul>
            <li>The symptoms of this incident</li>
            <li>The relevant logs</li>
            <li>The actual root cause</li>
            <li>The remediation that was performed</li>
            <li>The incident outcome</li>
            <li>The resolution time</li>
            <li>Engineer feedback</li>
        </ul>

        This information can be recalled when a similar
        incident occurs in the future.

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.success("The next similar incident can now benefit from this experience.")

    # ========================================================
    # LEARNING SUMMARY
    # ========================================================

    st.markdown("### 📚 Learning Summary")

    learn_col1, learn_col2, learn_col3 = st.columns(3)

    with learn_col1:
        st.metric(
            "Memory Created",
            "Yes",
        )

    with learn_col2:
        st.metric(
            "Outcome",
            outcome,
        )

    with learn_col3:
        st.metric(
            "Resolution Time",
            f"{resolution_time} min",
        )
