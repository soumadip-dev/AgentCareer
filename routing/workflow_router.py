"""
Workflow Router

Uses Gemini to intelligently select the most appropriate workflow
for a user's request.

Responsibilities:
1. Build the workflow routing prompt.
2. Retrieve available workflows from the workflow registry.
3. Ask Gemini to classify the user's request.
4. Return the selected workflow as a WorkflowDecision.
"""

from google.genai import types

from models.workflow_decision import WorkflowDecision
from routing.workflow_registry import WorkflowRegistry
from services.gemini_service import GeminiService


class WorkflowRouter:
    """
    LLM-powered workflow router.

    Uses Gemini to analyze a user's request and select
    the most appropriate workflow from the registered workflows.
    """

    def __init__(
        self,
        gemini_service: GeminiService,
        workflow_registry: WorkflowRegistry,
    ) -> None:
        """
        Initialize the workflow router.

        Args:
            gemini_service: Service used to communicate with Gemini.
            workflow_registry: Registry containing the available workflows.
        """
        self.gemini = gemini_service
        self.registry = workflow_registry

    def route(self, user_query: str) -> WorkflowDecision:
        """
        Determine the most appropriate workflow for a user request.

        Args:
            user_query: The user's request.

        Returns:
            WorkflowDecision: The workflow selected by Gemini.

        Raises:
            RuntimeError: If the Gemini API request fails.
        """
        prompt = self.build_prompt(user_query)

        response = self.gemini.generate_response(
            prompt=prompt,
            config=types.GenerateContentConfig(
                # Request a structured JSON response that matches
                # the WorkflowDecision schema.
                response_mime_type="application/json",
                response_schema=WorkflowDecision,
            ),
        )

        return response.parsed

    def build_prompt(self, user_query: str) -> str:
        """
        Build the prompt used to route the user's request.

        Args:
            user_query: The user's request.

        Returns:
            str: The workflow routing prompt.
        """
        workflow_details = []

        for workflow in self.registry.get_available_workflows():
            workflow_details.append(f"- {workflow}")

        available_workflows = "\n".join(workflow_details)

        prompt = f"""
You are an enterprise AI workflow router.

Your task is to analyze the user's request and select the
single most appropriate workflow from the available workflows.

Available Workflows:
{available_workflows}

Routing Instructions:
1. Select exactly ONE workflow.
2. The selected workflow_name MUST match one of the available workflows exactly.
3. Choose the workflow that best matches the user's primary intent.
4. Set confidence to a clear confidence level such as "high", "medium", or "low".
5. Provide a brief reason explaining why the selected workflow is appropriate.
6. Return the result using ONLY the provided WorkflowDecision schema.
7. Do not return any additional text outside the schema.

User Request:
{user_query}
"""

        return prompt
