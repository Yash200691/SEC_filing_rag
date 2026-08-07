"""
Context Builder for Financial RAG.

Converts retrieved search results into
a clean context string for the LLM.
"""

from typing import Dict, List

from retriever.tokenizer import GrokTokenizer
from retriever.formatter import ContextFormatter

class ContextBuilder:
    """
    Builds LLM context from retrieved chunks.
    """

    def __init__(self):
        self.tokenizer = GrokTokenizer()
        self.formatter = ContextFormatter()
    def build(
        self,
        results: List[Dict],
        max_tokens: int = 6000,
    ) -> Dict:
        """
        Build the final context while respecting
        the token budget.
        """

        if not results:
            return {
                "context": "",
                "tokens_used": 0,
                "chunks_used": 0,
                "chunks_skipped": 0,
            }

        contexts = []

        current_tokens = 0

        chunks_used = 0

        for idx, result in enumerate(results, start=1):

            payload = result["payload"]

            context = self.formatter.format(
                payload,
                idx
            )

            tokens = self.tokenizer.count_tokens(context)

            # Stop if token budget is exceeded
            if current_tokens + tokens > max_tokens:
                break

            contexts.append(context)

            current_tokens += tokens
            chunks_used += 1

        return {
            "context": "\n\n" + ("-" * 80) + "\n\n".join(contexts),
            "tokens_used": current_tokens,
            "chunks_used": chunks_used,
            "chunks_skipped": len(results) - chunks_used,
        }