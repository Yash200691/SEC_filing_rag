"""
Tokenizer utilities for RAG.

Responsible only for counting tokens.
"""

from abc import ABC, abstractmethod


class BaseTokenizer(ABC):
    """
    Abstract tokenizer interface.
    """

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        pass

class GrokTokenizer(BaseTokenizer):
    """
    Approximate tokenizer for Grok models.
    """

    CHARS_PER_TOKEN = 4

    def count_tokens(self, text: str) -> int:
        return max(1, len(text) // self.CHARS_PER_TOKEN)