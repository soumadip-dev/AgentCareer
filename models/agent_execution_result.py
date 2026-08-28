"""
Agent execution result.

Represents the execution details of an AI agent.

Responsibilities:
1. Store execution status.
2. Store retry attempts.
3. Store execution duration.
4. Display execution summary.
"""

from dataclasses import dataclass
from typing import Optional

from rich import print


@dataclass
class AgentExecutionResult:
    """
    Store execution details for an AI agent.
    """

    agent_name: str
    status: str
    attempts: int
    execution_duration: float
    error_message: Optional[str] = None

    def display(self) -> None:
        """
        Display execution details.
        """
        print(f"[bold yellow]Agent Name        :[/bold yellow] {self.agent_name}")
        print(f"[bold yellow]Status            :[/bold yellow] {self.status}")
        print(f"[bold yellow]Attempts          :[/bold yellow] {self.attempts}")
        print(
            f"[bold yellow]Execution Duration:[/bold yellow] "
            f"{self.execution_duration:.2f} seconds"
        )

        if self.error_message:
            print(f"[bold red]Error Message     :[/bold red] " f"{self.error_message}")
