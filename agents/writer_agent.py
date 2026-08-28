"""
Writer Agent

Responsibility:
Convert the research output into a professional career roadmap.
"""

from agents.base_agent import BaseAgent
from prompts.writer_prompt import WRITER_PROMPT


class WriterAgent(BaseAgent):

    def get_agent_name(self) -> str:
        return "Writer"

    def get_memory_key(self) -> str:
        return "writer"

    def build_prompt(self) -> str:
        research_response = self.memory.get("researcher")
        return WRITER_PROMPT.format(research_output=research_response)
