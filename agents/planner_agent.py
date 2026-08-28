"""
Planner Agent

Responsibility:
Create the initial learning plan based on the user's career goal.
"""

from agents.base_agent import BaseAgent
from prompts.planner_prompt import PLANNER_PROMPT


class PlannerAgent(BaseAgent):
    def get_agent_name(self) -> str:
        return "Planner"

    def get_memory_key(self) -> str:
        return "planner"

    def build_prompt(self) -> str:
        user_query = self.memory.get("user_query")
        return PLANNER_PROMPT.format(user_query=user_query)
