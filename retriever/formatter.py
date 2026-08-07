"""
Formatting utilities for retrieved documents.
"""

from typing import Dict


class ContextFormatter:
    """
    Formats retrieved payloads into
    readable text for the LLM.
    """

    def format(
        self,
        payload: Dict,
        source_number: int,
    ) -> str:

        company = payload.get("company", "Unknown")

        year = payload.get("year", "Unknown")

        section = payload.get("section", "Unknown")

        text = payload.get("text", "")

        return (
            f"Source {source_number}\n"
            f"Company: {company}\n"
            f"Year: {year}\n"
            f"Section: {section}\n\n"
            f"{text}"
        )