"""
AgentCareer Streamlit Application

Provides the web interface for the AgentCareer multi-agent
AI career coaching system.
"""

import streamlit as st

from backend_logic import main

# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AgentCareer",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Session State
# ---------------------------------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "workflow" not in st.session_state:
    st.session_state.workflow = "Idle"

if "status" not in st.session_state:
    st.session_state.status = "Ready"


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.title("AgentCareer 🧭")

    # Application status
    if st.session_state.status == "Ready":
        st.success("🟢 Ready")
    elif st.session_state.status == "Running":
        st.info("🔵 Workflow Running")
    else:
        st.error("🔴 Error")

    st.divider()

    # Conversation History
    st.subheader("📄 Conversation History")

    if not st.session_state.history:
        st.info("No conversation yet.")
    else:
        for index, query in enumerate(
            reversed(st.session_state.history),
            start=1,
        ):
            st.caption(f"{index}. {query}")

    st.divider()

    # System Information
    st.subheader("⚙️ System Information")

    st.write("Backend: Connected")
    st.write(f"Workflow: {st.session_state.workflow}")
    st.write("Memory: Session Active")


# ---------------------------------------------------------------------------
# Main Page
# ---------------------------------------------------------------------------

st.title("AgentCareer 🧭")
st.caption("Enterprise Multi-Agent AI Application")

st.divider()


# ---------------------------------------------------------------------------
# User Input
# ---------------------------------------------------------------------------

st.subheader("✨ Career Goal")

user_query = st.text_area(
    "Enter your career goal",
    height=150,
    placeholder="Example: I want to become an AI engineer",
)

generate = st.button(
    "Generate Career Roadmap",
    type="primary",
    use_container_width=True,
)


# ---------------------------------------------------------------------------
# Execute Workflow
# ---------------------------------------------------------------------------

if generate:
    user_query = user_query.strip()

    if not user_query:
        st.warning("Please enter your career goal.")

    else:
        # Store query in conversation history.
        st.session_state.history.append(user_query)

        # Update application status.
        st.session_state.status = "Running"
        st.session_state.workflow = "Processing..."

        try:
            # Execute the multi-agent workflow.
            with st.spinner("Executing Multi-Agent Workflow..."):
                final_response = main(user_query)

            # Update application status.
            st.session_state.status = "Ready"
            st.session_state.workflow = "Completed"

            st.success("Workflow executed successfully.")

            st.divider()

            # Display final response.
            st.subheader("🤖 AI Career Coach")

            st.markdown(final_response.output)

        except Exception as error:
            # Update application status.
            st.session_state.status = "Error"
            st.session_state.workflow = "Failed"

            st.error("An error occurred while executing the workflow.")

            st.exception(error)
