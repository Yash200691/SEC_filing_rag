"""
Production RAG Pipeline.

Coordinates retrieval, context building,
prompt creation and LLM generation.
"""

from retriever.search import SearchEngine
from retriever.context_builder import ContextBuilder
from retriever.prompt_builder import PromptBuilder
from retriever.LLM import GrokLLM


class RAGPipeline:
    """
    Main RAG Pipeline.
    """

    def __init__(self):

        self.search_engine = SearchEngine()

        self.context_builder = ContextBuilder()

        self.prompt_builder = PromptBuilder()

        self.llm = GrokLLM()

    def ask(
        self,
        question: str,
        top_k: int = 5,
    ) -> str:
        """
        Execute the complete RAG pipeline.

        Steps:
        1. Search
        2. Build Context
        3. Build Prompt
        4. Generate Answer
        """

        # Step 1
        search_results = self.search_engine.search(
            question=question,
            top_k=top_k,
        )

        print("=" * 80)
        print("SEARCH RESULTS")
        print("=" * 80)
        print(search_results)

        # Step 2
        context = self.context_builder.build(
            search_results
        )

        # Step 3
        prompt = self.prompt_builder.build(
            question=question,
            context=context,
        )

        # Step 4
        answer = self.llm.generate(
            prompt
        )

        return answer