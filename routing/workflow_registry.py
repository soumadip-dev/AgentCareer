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

from rich import print


class WorkflowRegistry:
    """
    Stores and manages all workflows supported by the application.
    """

    def __init__(self) -> None:
        """
        Initialize the workflow registry with the default workflows.
        """
        self._workflows: dict[str, list[str]] = {
            "roadmap": ["planner", "researcher", "writer", "reviewer"],
            "certification": ["researcher", "writer"],
            "project": ["researcher", "writer"],
            "review": ["reviewer"],
        }

    def get_workflow(self, workflow_name: str) -> list[str]:
        """
        Retrieve the ordered list of agents for a workflow.

        Args:
            workflow_name: Name of the workflow to retrieve.

        Returns:
            A list of agent names in execution order.

        Raises:
            ValueError: If the requested workflow is not registered.
        """
        workflow_name = workflow_name.lower()

        if not self.workflow_exists(workflow_name):
            raise ValueError(f"Workflow '{workflow_name}' is not registered.")

        # Return a copy to prevent external code from modifying
        # the workflow stored inside the registry.
        return self._workflows[workflow_name].copy()

    def workflow_exists(self, workflow_name: str) -> bool:
        """
        Check whether a workflow is registered.

        Args:
            workflow_name: Name of the workflow to check.

        Returns:
            True if the workflow exists, otherwise False.
        """
        return workflow_name.lower() in self._workflows

    def get_available_workflows(self) -> list[str]:
        """
        Return the names of all registered workflows.

        Returns:
            A list containing all registered workflow names.
        """
        return list(self._workflows.keys())

    def register_workflow(
        self,
        workflow_name: str,
        agents: list[str],
    ) -> None:
        """
        Register a new workflow.

        Args:
            workflow_name: Name of the workflow to register.
            agents: Ordered list of agent names to execute.

        Raises:
            ValueError: If a workflow with the same name already exists.
        """
        workflow_name = workflow_name.lower()
        agents = [agent.lower() for agent in agents]

        if self.workflow_exists(workflow_name):
            raise ValueError(f"Workflow '{workflow_name}' already exists.")

        self._workflows[workflow_name] = agents

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
            for workflow_name, agents in self._workflows.items():
                print(
                    f"\n[bold green]Workflow:[/bold green] "
                    f"[bold white]{workflow_name.title()}[/bold white]"
                )

                for index, agent in enumerate(agents, start=1):
                    print(
                        f"  [bold yellow]{index}.[/bold yellow] "
                        f"[blue]{agent.title()} Agent[/blue]"
                    )

        print(f"\n[bold cyan]{separator}[/bold cyan]\n")
