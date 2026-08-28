"""
Certification Agent

Responsibility:
Recommend relevant industry certifications based on the user's career goal.
"""

from agents.base_agent import BaseAgent
from prompts.certification_prompt import CERTIFICATION_PROMPT


class CertificationAgent(BaseAgent):

    def get_agent_name(self) -> str:
        return "Certification"

    def get_memory_key(self) -> str:
        return "certification"

    def build_prompt(self) -> str:
        user_query = self.memory.get("user_query")
        return CERTIFICATION_PROMPT.format(user_query=user_query)
