"""
Workflow Decision

Represents the routing decision returned by the workflow router.

Responsibilities:
1. Store the selected workflow.
2. Store the routing confidence.
3. Store the reason for selecting the workflow.
"""

from dataclasses import dataclass

from rich import print


@dataclass
class WorkflowDecision:
    """
    Represents the result of a workflow routing decision.

    Attributes:
        workflow_name: Name of the workflow selected by the router.
        confidence: Confidence level of the routing decision.
        reason: Explanation for selecting the workflow.
    """

    workflow_name: str
    confidence: str
    reason: str

    def display(self) -> None:
        """
        Display the workflow routing decision using Rich.
        """
        separator = "=" * 70

        print(f"[dim]{separator}[/dim]")
        print("[bold cyan]WORKFLOW DECISION[/bold cyan]")
        print(f"[dim]{separator}[/dim]")

        print(f"[bold]Workflow:[/bold] {self.workflow_name}")
        print(f"[bold]Confidence:[/bold] {self.confidence}")
        print(f"[bold]Reason:[/bold] {self.reason}")

        print(f"[dim]{separator}[/dim]")
