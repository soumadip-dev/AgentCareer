"""
Research Agent

Responsibility:
Perform detailed research based on the planner's execution plan.
"""

from agents.base_agent import BaseAgent
from knowledge.knowledge_base import KnowledgeBase
from memory.conversation_memory import ConversationMemory
from memory.shared_memory import SharedMemory
from prompts.research_prompt import RESEARCH_PROMPT
from services.gemini_service import GeminiService


class ResearchAgent(BaseAgent):

    # Used only to test the retry mechanism.
    def __init__(
        self,
        memory: SharedMemory,
        conversation_memory: ConversationMemory,
        gemini_service: GeminiService,
        knowledge_base: KnowledgeBase,
    ) -> None:
        super().__init__(
            memory,
            conversation_memory,
            gemini_service,
            knowledge_base,
        )
        self.counter = 0

    def get_agent_name(self) -> str:
        return "Researcher"

    def get_memory_key(self) -> str:
        return "researcher"

    def build_prompt(self) -> str:
        # Intentionally fail the first two attempts to test the retry mechanism.
        self.counter += 1

        if self.counter < 3:
            raise RuntimeError(
                "Simulated research agent failure for retry mechanism testing."
            )

        planner_response = self.memory.get("planner")

        return RESEARCH_PROMPT.format(planner_output=planner_response)
