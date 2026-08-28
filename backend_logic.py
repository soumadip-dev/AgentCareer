"""
AgentCareer Backend

Provides the application logic for the AgentCareer multi-agent
AI career coaching system.

This module is responsible for:

1. Initializing shared services and memory.
2. Creating and registering AI agents.
3. Routing user queries to the appropriate workflow.
4. Executing the selected workflow.
5. Returning the final agent response.

The user interface is handled separately by Streamlit.
"""

from agents.certification_agent import CertificationAgent
from agents.planner_agent import PlannerAgent
from agents.project_agent import ProjectAgent
from agents.research_agent import ResearchAgent
from agents.reviewer_agent import ReviewerAgent
from agents.writer_agent import WriterAgent
from knowledge.knowledge_base import KnowledgeBase
from memory.conversation_memory import ConversationMemory
from memory.shared_memory import SharedMemory
from models.agent_response import AgentResponse
from orchestrator.agent_orchestrator import AgentOrchestrator
from routing.workflow_registry import WorkflowRegistry
from routing.workflow_router import WorkflowRouter
from services.gemini_service import GeminiService


def main(user_query: str) -> AgentResponse:
    """
    Execute the AgentCareer multi-agent workflow.

    Args:
        user_query: Career-related question or goal provided
            by the user.

    Returns:
        AgentResponse containing the final response generated
        by the selected workflow.

    Raises:
        ValueError: If the user query is empty.
    """

    # -----------------------------------------------------------------------
    # Validate Input
    # -----------------------------------------------------------------------

    user_query = user_query.strip()

    if not user_query:
        raise ValueError("Career goal cannot be empty.")

    # -----------------------------------------------------------------------
    # Initialize Shared Services
    # -----------------------------------------------------------------------

    conversation_memory = ConversationMemory()
    gemini_service = GeminiService()
    knowledge_base = KnowledgeBase("data/career_knowledge.json")

    # -----------------------------------------------------------------------
    # Initialize Workflow Components
    # -----------------------------------------------------------------------

    workflow_registry = WorkflowRegistry()

    workflow_router = WorkflowRouter(
        gemini_service,
        workflow_registry,
    )

    # -----------------------------------------------------------------------
    # Initialize Memory
    # -----------------------------------------------------------------------

    memory = SharedMemory()

    conversation_memory.add_user_message(user_query)
    memory.add("user_query", user_query)

    # -----------------------------------------------------------------------
    # Initialize Agents
    # -----------------------------------------------------------------------

    planner = PlannerAgent(
        memory,
        conversation_memory,
        gemini_service,
        knowledge_base,
    )

    researcher = ResearchAgent(
        memory,
        conversation_memory,
        gemini_service,
        knowledge_base,
    )

    writer = WriterAgent(
        memory,
        conversation_memory,
        gemini_service,
        knowledge_base,
    )

    reviewer = ReviewerAgent(
        memory,
        conversation_memory,
        gemini_service,
        knowledge_base,
    )

    project = ProjectAgent(
        memory,
        conversation_memory,
        gemini_service,
        knowledge_base,
    )

    certification = CertificationAgent(
        memory,
        conversation_memory,
        gemini_service,
        knowledge_base,
    )

    # -----------------------------------------------------------------------
    # Initialize Orchestrator
    # -----------------------------------------------------------------------

    orchestrator = AgentOrchestrator(
        memory,
        conversation_memory,
    )

    # Register all available agents.
    orchestrator.register(planner)
    orchestrator.register(researcher)
    orchestrator.register(writer)
    orchestrator.register(reviewer)
    orchestrator.register(project)
    orchestrator.register(certification)

    # -----------------------------------------------------------------------
    # Route User Query
    # -----------------------------------------------------------------------

    decision = workflow_router.route(user_query)

    # -----------------------------------------------------------------------
    # Retrieve Selected Workflow
    # -----------------------------------------------------------------------

    workflow = workflow_registry.get_workflow(decision.workflow_name)

    # -----------------------------------------------------------------------
    # Execute Workflow
    # -----------------------------------------------------------------------

    final_response = orchestrator.execute(workflow)

    # -----------------------------------------------------------------------
    # Store Final Response
    # -----------------------------------------------------------------------

    conversation_memory.add_ai_message(final_response.output)

    return final_response
