"""
Agent Orchestrator

Coordinates the registration and sequential execution of AI agents
within a selected workflow.

The orchestrator is responsible for:
1. Registering available AI agents.
2. Executing agents in the order defined by a workflow.
3. Passing shared state through the agent workflow.
4. Returning the response produced by the final agent.
5. Retrying failed agent executions.
6. Tracking execution details.
7. Returning the final response.
"""

import time

from rich import print

from agents.base_agent import BaseAgent
from memory.conversation_memory import ConversationMemory
from memory.shared_memory import SharedMemory
from models.agent_execution_result import AgentExecutionResult
from models.agent_response import AgentResponse


class AgentOrchestrator:
    """
    Manages and executes AI agents in a defined sequence.
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
        self._execution_results: list[AgentExecutionResult] = []

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

        self._execution_results.clear()

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
        Execute an agent with retry attempts.

        Args:
            agent: AI agent instance.

        Returns:
            AgentResponse: The response produced by the agent.

        Raises:
            RuntimeError: If the agent fails after all retry attempts.
        """
        start_time = time.perf_counter()
        last_exception = None

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                print(
                    f"\n[bold blue]Attempt {attempt}/{self.MAX_RETRIES}:[/bold blue] "
                    f"Executing [bold white]"
                    f"{agent.get_agent_name()} Agent"
                    f"[/bold white]..."
                )

                response = agent.execute()

                execution_time = time.perf_counter() - start_time

                self._execution_results.append(
                    AgentExecutionResult(
                        agent_name=agent.get_agent_name(),
                        status="SUCCESS",
                        attempts=attempt,
                        execution_duration=execution_time,
                    )
                )

                print("[bold green]Success![/bold green]")

                return response

            except Exception as ex:
                last_exception = ex

                print(
                    f"[bold red]Attempt {attempt} failed.[/bold red]"
                    f"\n[red]Error: {ex}[/red]"
                )

                # Stop retrying when the maximum number of attempts is reached.
                if attempt == self.MAX_RETRIES:
                    break

                # Use exponential backoff between retry attempts:
                # Attempt 1 -> 1 second
                # Attempt 2 -> 2 seconds
                retry_delay = 2 ** (attempt - 1)

                print(f"[yellow]Retrying in " f"{retry_delay} second(s)...[/yellow]")

                time.sleep(retry_delay)

        execution_time = time.perf_counter() - start_time

        self._execution_results.append(
            AgentExecutionResult(
                agent_name=agent.get_agent_name(),
                status="FAILED",
                attempts=self.MAX_RETRIES,
                execution_duration=execution_time,
                error_message=str(last_exception),
            )
        )

        raise RuntimeError(
            f"Failed to execute "
            f"{agent.get_agent_name()} agent "
            f"after {self.MAX_RETRIES} attempts."
        ) from last_exception

    def get_execution_results(self) -> list[AgentExecutionResult]:
        """
        Return the execution Summary.
        """
        return self._execution_results

    def display_execution_summary(self) -> None:
        """
        Display the execution summary.
        """
        print(f"\n[dim]{'=' * 70}[/dim]")
        print("[bold cyan]MULTI-AGENT WORKFLOW EXECUTION SUMMARY[/bold cyan]")
        print(f"[dim]{'=' * 70}[/dim]\n")

        for result in self._execution_results:
            result.display()
            print(f"\n[dim]{'-' * 70}[/dim]")
        print(f"[dim]{'=' * 70}[/dim]")
