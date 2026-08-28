"""
Workflow Registry

Maintains all workflows supported by the AI Career Coach application.

Responsibilities:
1. Register available workflows.
2. Retrieve a workflow by name.
3. Validate whether a workflow exists.
4. Return the list of available workflows.
5. Display all registered workflows.
"""

from typing import TypeAlias

from rich import print

WorkflowStep: TypeAlias = str | list[str]
Workflow: TypeAlias = list[WorkflowStep]


class WorkflowRegistry:
    """
    Stores and manages all workflows supported by the application.
    """

    def __init__(self) -> None:
        """
        Initialize the workflow registry with the default workflows.
        """
        self._workflows: dict[str, Workflow] = {
            "roadmap": [
                "planner",
                ["researcher", "project", "certification"],
                "writer",
                "reviewer",
            ],
            "certification": [
                "researcher",
                "writer",
            ],
            "project": [
                "researcher",
                "writer",
            ],
            "review": [
                "reviewer",
            ],
        }

    def get_workflow(self, workflow_name: str) -> Workflow:
        """
        Retrieve the workflow by name.

        Args:
            workflow_name: Name of the workflow to retrieve.

        Returns:
            Workflow containing sequential agents and/or parallel agent groups.

        Raises:
            ValueError: If the requested workflow is not registered.
        """
        workflow_name = workflow_name.lower()

        if not self.workflow_exists(workflow_name):
            raise ValueError(f"Workflow '{workflow_name}' is not registered.")

        # Return a copy to prevent external modification.
        return self._workflows[workflow_name].copy()

    def workflow_exists(self, workflow_name: str) -> bool:
        """
        Check whether a workflow exists.

        Args:
            workflow_name: Name of the workflow to check.

        Returns:
            True if the workflow exists, otherwise False.
        """
        return workflow_name.lower() in self._workflows

    def get_available_workflows(self) -> list[str]:
        """
        Return the names of all registered workflows.
        """
        return list(self._workflows.keys())

    def register_workflow(
        self,
        workflow_name: str,
        agents: Workflow,
    ) -> None:
        """
        Register a new workflow.

        Args:
            workflow_name: Name of the workflow.
            agents: Workflow steps containing sequential agents
                and/or parallel agent groups.

        Raises:
            ValueError: If a workflow with the same name already exists.
        """
        workflow_name = workflow_name.lower()

        if self.workflow_exists(workflow_name):
            raise ValueError(f"Workflow '{workflow_name}' already exists.")

        normalized_agents: Workflow = []

        for agent in agents:
            if isinstance(agent, list):
                normalized_agents.append([name.lower().strip() for name in agent])
            else:
                normalized_agents.append(agent.lower().strip())

        self._workflows[workflow_name] = normalized_agents

    def display(self) -> None:
        """
        Display all registered workflows using Rich.
        """
        separator = "=" * 70

        print(f"\n[bold cyan]{separator}[/bold cyan]")
        print("[bold magenta]WORKFLOW REGISTRY[/bold magenta]")
        print(f"[bold cyan]{separator}[/bold cyan]")

        if not self._workflows:
            print(
                "[italic yellow]No workflows are currently registered.[/italic yellow]"
            )
        else:
            for workflow_name, steps in self._workflows.items():
                print(
                    f"\n[bold green]Workflow:[/bold green] "
                    f"[bold white]{workflow_name.title()}[/bold white]"
                )

                for index, step in enumerate(steps, start=1):

                    if isinstance(step, list):
                        agents = ", ".join(agent.title() for agent in step)

                        print(
                            f"  [bold yellow]{index}.[/bold yellow] "
                            f"[blue]Parallel:[/blue] "
                            f"[blue]{agents}[/blue]"
                        )
                    else:
                        print(
                            f"  [bold yellow]{index}.[/bold yellow] "
                            f"[blue]{step.title()} Agent[/blue]"
                        )

        print(f"\n[bold cyan]{separator}[/bold cyan]\n")
