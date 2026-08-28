"""
Project Agent

Responsibility: Recommend relevant projects based on the user's career goal.
1. Suggest beginner level projects.
2. Suggest intermediate level projects.
3. Suggest advanced level projects.
"""

from agents.base_agent import BaseAgent
from prompts.project_prompt import PROJECT_PROMPT


class ProjectAgent(BaseAgent):
    def get_agent_name(self) -> str:
        return "Project"

    def get_memory_key(self) -> str:
        return "project"

    def build_prompt(self) -> str:
        user_query = self.memory.get("user_query")
        return PROJECT_PROMPT.format(user_query=user_query)
