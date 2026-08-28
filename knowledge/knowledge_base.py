"""
Knowledge Base

Provides domain-specific knowledge to AI agents.

Responsibilities:
1. Load domain-specific knowledge from a JSON file.
2. Retrieve knowledge using a specific key.
3. Hide the underlying data source from AI agents.
4. Provide a simple interface for accessing stored knowledge.
5. Prepare the application for future Retrieval-Augmented Generation (RAG)
   implementation.
"""

import json
from pathlib import Path
from typing import Any

from rich import print


class KnowledgeBase:
    """
    Load and manage domain-specific knowledge.

    Currently, knowledge is loaded from a JSON file. The implementation
    can later be extended or replaced with a vector database as part of
    a Retrieval-Augmented Generation (RAG) system.
    """

    def __init__(self, knowledge_file: str) -> None:
        """
        Initialize the knowledge base.

        Args:
            knowledge_file: Path to the JSON file containing the
                domain-specific knowledge.
        """
        self._knowledge = self._load_knowledge(knowledge_file)

    def _load_knowledge(self, knowledge_file: str) -> dict[str, Any]:
        """
        Load knowledge from a JSON file.

        Args:
            knowledge_file: Path to the JSON file containing the
                knowledge base.

        Returns:
            A dictionary containing the loaded knowledge.

        Raises:
            FileNotFoundError: If the knowledge file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        file_path = Path(knowledge_file)

        if not file_path.exists():
            raise FileNotFoundError(f"Knowledge base file not found: {knowledge_file}")

        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def get(self, key: str) -> Any:
        """
        Retrieve knowledge using a specific key.

        Args:
            key: The key used to look up the knowledge.

        Returns:
            The knowledge associated with the key, or None if the key
            does not exist.
        """
        return self._knowledge.get(key)

    def retrieve(self, query: str) -> dict[str, Any]:
        """
        Retrieve knowledge relevant to the given query.

        The query and knowledge-base keys are normalized before matching.
        Hyphens and underscores are replaced with spaces so that variations
        such as "ai-engineer", "ai_engineer", and "AI Engineer" can be
        matched consistently.

        Args:
            query: The query used to search the knowledge base.

        Returns:
            The matching knowledge entry, or an empty dictionary if no
            relevant knowledge is found.
        """

        # Normalize the query for consistent keyword matching.
        normalized_query = query.lower().replace("-", " ").replace("_", " ").strip()

        # Check each knowledge-base entry against the normalized query.
        for key, value in self._knowledge.items():
            normalized_key = key.lower().replace("-", " ").replace("_", " ").strip()

            # Return the knowledge entry when its key is found in the query.
            if normalized_key in normalized_query:
                return value

        # No matching knowledge entry was found.
        return {}

    def get_all(self) -> dict[str, Any]:
        """
        Retrieve all stored knowledge.

        Returns:
            A copy of the complete knowledge base.
        """
        return self._knowledge.copy()

    def exists(self, key: str) -> bool:
        """
        Check whether a key exists in the knowledge base.

        Args:
            key: The key to check.

        Returns:
            True if the key exists; otherwise, False.
        """
        return key in self._knowledge

    def display(self) -> None:
        """
        Display the available knowledge base keys using Rich.

        This method is primarily useful for debugging and inspecting
        the contents of the knowledge base.
        """
        separator = "=" * 70

        print(f"\n[dim]{separator}[/dim]")
        print("[bold cyan]Knowledge Base[/bold cyan]")
        print(f"[dim]{separator}[/dim]")

        if not self._knowledge:
            print("[italic yellow]Knowledge base is currently empty.[/italic yellow]")
        else:
            print("[bold green]Available Knowledge:[/bold green]")

            for key in self._knowledge:
                print(f"  [bold cyan]•[/bold cyan] [white]{key}[/white]")

        print(f"[dim]{separator}[/dim]\n")
