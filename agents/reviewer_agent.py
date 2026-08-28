"""
Reviewer Agent

Responsibility:
Review and improve the career roadmap.
"""

from agents.base_agent import BaseAgent
from prompts.reviewer_prompt import REVIEWER_PROMPT


class ReviewerAgent(BaseAgent):

    def get_agent_name(self) -> str:
        return "Reviewer"

    def get_memory_key(self) -> str:
        return "reviewer"

    def build_prompt(self) -> str:
        writer_response = self.memory.get("writer")
        return REVIEWER_PROMPT.format(roadmap=writer_response)
