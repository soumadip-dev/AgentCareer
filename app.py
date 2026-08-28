"""
AI Career Coach

Entry point of the application.
Initializes the required services and agents, executes the career
roadmap workflow, and displays the final result.
"""

from rich import print

from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.reviewer_agent import ReviewerAgent

from memory.shared_memory import SharedMemory
from services.gemini_service import GeminiService


def main() -> None:
    """
    Run the AI Career Coach application.

    Workflow:
        1. Get the user's career goal.
        2. Initialize shared memory and Gemini service.
        3. Create all career planning agents.
        4. Execute each agent in sequence.
        5. Display the final career roadmap.
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

    # Store the user's career goal so all agents can access it.
    memory.add("user_query", user_query)

    # Initialize all agents with the shared memory and Gemini service.
    planner = PlannerAgent(memory, gemini_service)
    researcher = ResearchAgent(memory, gemini_service)
    writer = WriterAgent(memory, gemini_service)
    reviewer = ReviewerAgent(memory, gemini_service)

    # Execute the career planning workflow.
    print("\n[bold blue]1. Planning[/bold blue]  Creating your career roadmap...")
    planner.execute()

    print("[bold blue]2. Research[/bold blue]  Researching relevant technologies...")
    researcher.execute()

    print("[bold blue]3. Writing[/bold blue]  Preparing the professional roadmap...")
    writer.execute()

    print("[bold blue]4. Review[/bold blue]  Reviewing and improving the roadmap...")
    reviewer.execute()

    # Retrieve the final reviewed roadmap from shared memory.
    final_response = memory.get("reviewer")

    # Display the final career roadmap.
    print("\n" + "[dim]" + "=" * 70 + "[/dim]")
    print("[bold green]FINAL CAREER ROADMAP[/bold green]")
    print("[dim]" + "=" * 70 + "[/dim]")
    print(final_response.output)


if __name__ == "__main__":
    main()
