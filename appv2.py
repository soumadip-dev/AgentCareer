"""
AI Career Coach

Entry point of the application.
"""

from rich import print

from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.reviewer_agent import ReviewerAgent

from orchestrator.agent_orchestrator import AgentOrchestrator

from memory.shared_memory import SharedMemory
from services.gemini_service import GeminiService


def main() -> None:
    """
    Run the AI Career Coach application.

    Workflow:
        1. Get the user's career goal.
        2. Initialize shared memory and the Gemini service.
        3. Create the career planning agents.
        4. Register the agents with the orchestrator.
        5. Execute the agents in sequence.
        6. Display the final career roadmap.
    """

    # Display the application header.
    print("\n" + "[dim]" + "=" * 70 + "[/dim]")
    print("[bold cyan]AI Career Coach[/bold cyan]")
    print("[dim]" + "=" * 70 + "[/dim]")

    # Get the user's career goal.
    user_query = input("Enter your career goal: ")

    # Initialize shared memory and the Gemini service.
    memory = SharedMemory()
    gemini_service = GeminiService()

    # Store the user's career goal in shared memory
    # so that the agents can access it when building their prompts.
    memory.add("user_query", user_query)

    # Create all agents using the shared memory and Gemini service.
    planner = PlannerAgent(memory, gemini_service)
    researcher = ResearchAgent(memory, gemini_service)
    writer = WriterAgent(memory, gemini_service)
    reviewer = ReviewerAgent(memory, gemini_service)

    # Create the orchestrator and register the agents
    # in the order in which they should be executed.
    orchestrator = AgentOrchestrator(memory)
    orchestrator.register(planner)
    orchestrator.register(researcher)
    orchestrator.register(writer)
    orchestrator.register(reviewer)

    # Execute the complete multi-agent workflow.
    final_response = orchestrator.execute()

    # Display the final reviewed career roadmap.
    print("\n" + "[dim]" + "=" * 70 + "[/dim]")
    print("[bold green]FINAL CAREER ROADMAP[/bold green]")
    print("[dim]" + "=" * 70 + "[/dim]")
    print(final_response.output)


if __name__ == "__main__":
    main()
