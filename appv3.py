"""
AI Career Coach

Entry point for the AI Career Coach application.

This module initializes the required services, knowledge base,
workflow components, and AI agents. It accepts career-related
queries from the user, routes each query to the appropriate
workflow, executes the selected multi-agent workflow, and
displays the final response.
"""

from rich import print

from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.reviewer_agent import ReviewerAgent
from agents.writer_agent import WriterAgent
from knowledge.knowledge_base import KnowledgeBase
from memory.conversation_memory import ConversationMemory
from memory.shared_memory import SharedMemory
from orchestrator.agent_orchestrator import AgentOrchestrator
from routing.workflow_registry import WorkflowRegistry
from routing.workflow_router import WorkflowRouter
from services.gemini_service import GeminiService


def main() -> None:
    """
    Run the AI Career Coach application.

    The application continuously accepts career-related queries
    until the user enters an exit command.

    Workflow:
        1. Initialize conversation memory, Gemini service,
           knowledge base, and workflow components.
        2. Display the application header.
        3. Get the user's career-related query.
        4. Check whether the user wants to exit.
        5. Validate the user input.
        6. Initialize shared memory for the current workflow.
        7. Store the user's query in conversation and shared memory.
        8. Create the required AI agents.
        9. Register the agents with the orchestrator.
        10. Route the query to the appropriate workflow.
        11. Execute the selected multi-agent workflow.
        12. Store the final response in conversation memory.
        13. Display the final response.
    """

    # Initialize components that are shared across user queries.
    conversation_memory = ConversationMemory()
    gemini_service = GeminiService()
    knowledge_base = KnowledgeBase("data/career_knowledge.json")

    # Initialize the workflow registry and router used to
    # select the appropriate workflow for each user query.
    workflow_registry = WorkflowRegistry()
    workflow_router = WorkflowRouter(
        gemini_service,
        workflow_registry,
    )

    while True:
        # Display the application header.
        separator = "=" * 70

        print(f"\n[dim]{separator}[/dim]")
        print("[bold cyan]AI Career Coach[/bold cyan]")
        print(f"[dim]{separator}[/dim]")

        # Get the user's career-related query.
        user_query = input("Enter your career goal: ").strip()

        # Exit the application when the user enters an exit command.
        if user_query.lower() in {"exit", "bye", "quit"}:
            print("[bold yellow]Exiting AI Career Coach...[/bold yellow]")
            break

        # Ignore empty input and prompt the user to enter a query.
        if not user_query:
            print("[italic yellow]" "Please enter a career goal." "[/italic yellow]")
            continue

        # Initialize shared memory for the current workflow.
        memory = SharedMemory()

        # Store the user's query in conversation memory so that
        # agents can access the conversation history.
        conversation_memory.add_user_message(user_query)

        # Store the user's query in shared memory so that agents
        # can access it while building their prompts.
        memory.add("user_query", user_query)

        # Create all AI agents using the shared memory,
        # conversation memory, Gemini service, and knowledge base.
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

        # Create the orchestrator with access to the shared
        # memory and conversation history.
        orchestrator = AgentOrchestrator(
            memory,
            conversation_memory,
        )

        # Register all available agents with the orchestrator.
        orchestrator.register(planner)
        orchestrator.register(researcher)
        orchestrator.register(writer)
        orchestrator.register(reviewer)

        # Route the user's query to the most appropriate workflow.
        decision = workflow_router.route(user_query)

        # Display the routing decision for debugging and visibility.
        decision.display()

        # Retrieve the ordered list of agents for the selected workflow.
        workflow = workflow_registry.get_workflow(decision.workflow_name)

        # Execute the selected multi-agent workflow.
        final_response = orchestrator.execute(workflow)

        # Store the final AI response in conversation memory so that
        # it is available as context for subsequent user queries.
        conversation_memory.add_ai_message(final_response.output)

        # Display the final response generated by the workflow.
        print(f"\n[dim]{separator}[/dim]")
        print("[bold green]FINAL RESPONSE[/bold green]")
        print(f"[dim]{separator}[/dim]")
        print(final_response.output)

        # Execution Summary
        orchestrator.display_execution_summary()


if __name__ == "__main__":
    main()
