"""
Agent Orchestrator

Coordinates the registration and sequential execution of AI agents
within a selected workflow.

The orchestrator is responsible for:
1. Registering available AI agents.
2. Executing agents in the order defined by a workflow.
3. Passing shared state through the agent workflow.
4. Returning the response produced by the final agent.
"""

from rich import print

from agents.base_agent import BaseAgent
from memory.conversation_memory import ConversationMemory
from memory.shared_memory import SharedMemory
from models.agent_response import AgentResponse


class AgentOrchestrator:
    """
    Manage and execute AI agents in a defined sequence.
    """

    MAX_RETRIES = 3

    def __init__(
        self,
        memory: SharedMemory,
        conversation_memory: ConversationMemory,
    ) -> None:
        """
        Initialize the agent orchestrator.

        Args:
            memory: Shared memory accessible by all agents.
            conversation_memory: Conversation history shared across agents.
        """
        self.memory = memory
        self.conversation_memory = conversation_memory
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """
        Register an AI agent with the orchestrator.

        The agent name is converted to lowercase before being used
        as the registry key.

        Args:
            agent: AI agent to register.
        """
        agent_name = agent.get_agent_name().lower().strip()
        self._agents[agent_name] = agent

    def execute(self, workflow: list[str]) -> AgentResponse:
        """
        Execute the agents in the order defined by the workflow.

        Args:
            workflow: Ordered list of agent names to execute.

        Returns:
            AgentResponse: The response produced by the final agent.

        Raises:
            ValueError: If an agent in the workflow is not registered.
            ValueError: If the workflow does not contain any agents.
        """
        if not workflow:
            raise ValueError("Workflow cannot be empty.")

        separator = "=" * 70

        print(f"\n[dim]{separator}[/dim]")
        print("[bold cyan]STARTING MULTI-AGENT WORKFLOW[/bold cyan]")
        print(f"[dim]{separator}[/dim]")

        final_response: AgentResponse

        for step, agent_name in enumerate(workflow, start=1):
            normalized_name = agent_name.lower().strip()
            agent = self._agents.get(normalized_name)

            if agent is None:
                raise ValueError(f"Agent '{agent_name}' is not registered.")

            print(
                f"\n[bold blue]Step {step}:[/bold blue] "
                f"Executing [bold white]"
                f"{agent.get_agent_name()} Agent"
                f"[/bold white]..."
            )

            # final_response = agent.execute()
            final_response = self._execute_with_retry(agent)

        print(f"\n[dim]{separator}[/dim]")
        print("[bold green]MULTI-AGENT WORKFLOW COMPLETED[/bold green]")
        print(f"[dim]{separator}[/dim]\n")

        return final_response

    def _execute_with_retry(self, agent: BaseAgent) -> AgentResponse:
        """
        Execute an agent with retries.

        Args:
            agent: AI agent instance.

        Returns:
            AgentResponse: The response produced by the agent.
        """
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                print(
                    f"\n[bold blue]Attempt {attempt}:[/bold blue] "
                    f"Executing [bold white]"
                    f"{agent.get_agent_name()} Agent"
                    f"[/bold white]..."
                )

                response = agent.execute()

                print("[bold green]Success![/bold green]")

                return response

            except Exception as ex:
                print(f"[bold red]Attempt {attempt} failed.[/bold red]")

                if attempt == self.MAX_RETRIES:
                    raise RuntimeError(
                        f"Failed to execute "
                        f"{agent.get_agent_name()} agent "
                        f"after {self.MAX_RETRIES} attempts."
                    ) from ex

                print(f"Retrying in {attempt}")

        raise RuntimeError(f"Failed to execute {agent.get_agent_name()} agent.")
