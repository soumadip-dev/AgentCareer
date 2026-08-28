"""
Agent Orchestrator

Coordinates the registration and sequential execution of AI agents
within a selected workflow.

The orchestrator is responsible for:
1. Registering available AI agents.
2. Executing agents in the order defined by a workflow.
3. Passing shared state through the agent workflow.
4. Requesting human approval before executing designated agents.
5. Allowing the user to cancel the workflow when approval is denied.
6. Returning the response produced by the final agent.
7. Retrying failed agent executions.
8. Tracking execution details.
9. Displaying the workflow execution summary.
"""

import time
from concurrent.futures import ThreadPoolExecutor

from rich import print

from agents.base_agent import BaseAgent
from memory.conversation_memory import ConversationMemory
from memory.shared_memory import SharedMemory
from models.agent_execution_result import AgentExecutionResult
from models.agent_response import AgentResponse

from routing.workflow_registry import Workflow


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
        self._approval_required_agents = {"reviewer"}

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

    def execute(self, workflow: Workflow) -> AgentResponse:
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
            if isinstance(agent_name, list):
                parallel_response = self._execute_parallel(agent_name)
                if parallel_response:
                    # Store the last response
                    final_response = parallel_response[-1]
            else:
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

                if agent_name.lower() in self._approval_required_agents:
                    approved = self._request_human_approval(agent)

                    if not approved:
                        print(
                            f"[bold red]"
                            f"Execution of {agent.get_agent_name()} Agent "
                            f"was cancelled by the user."
                            f"[/bold red]"
                        )

                        self._execution_results.append(
                            AgentExecutionResult(
                                agent_name=agent.get_agent_name(),
                                status="SKIPPED",
                                attempts=0,
                                execution_duration=0.0,
                                error_message="Execution was cancelled by the user.",
                            )
                        )

                        print("[bold red]Workflow stopped by user.[/bold red]")
                        break

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
            f"{agent.get_agent_name()} Agent "
            f"after {self.MAX_RETRIES} attempts."
        ) from last_exception

    def _execute_parallel(self, agent_names: list[str]):
        """ """
        print(
            f"\n[bold cyan]Executing {len(agent_names)} Agents in Parallel[/bold cyan]"
        )
        print(
            "[dim]Agents: " + ", ".join(name.title() for name in agent_names) + "[/dim]"
        )

        with ThreadPoolExecutor(max_workers=len(agent_names)) as executor:
            futures = []
            for agent_name in agent_names:
                agent = self._agents[agent_name.lower()]
                futures.append(executor.submit(self._execute_with_retry, agent))

        responses = []

        for future in futures:
            responses.append(future.result())

        return responses

    def _request_human_approval(self, agent: BaseAgent) -> bool:
        """
        Ask the user for approval before executing an AI agent.

        Args:
            agent: AI agent instance.

        Returns:
            bool: True if the user approves, False otherwise.
        """
        print(f"\n[dim]{'=' * 70}[/dim]")
        print("[bold cyan]Human Approval Required[/bold cyan]")
        print(f"[dim]{'=' * 70}[/dim]\n")

        print(f"[bold yellow]Agent Name:[/bold yellow] {agent.get_agent_name()}")

        while True:
            user_input = input("Approve? (Y/N): ").strip().lower()

            if user_input in {"y", "yes"}:
                return True

            elif user_input in {"n", "no"}:
                return False

            else:
                print("[red]Invalid input. Please enter 'Y' or 'N'.[/red]")

    def get_execution_results(self) -> list[AgentExecutionResult]:
        """
        Return the execution summary.
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
