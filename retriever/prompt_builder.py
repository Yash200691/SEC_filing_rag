"""
Prompt Builder

Builds prompts for the LLM.
"""


class PromptBuilder:

    SYSTEM_PROMPT = """
You are an expert financial analyst.

Use ONLY the supplied context to answer.

If the answer cannot be found,
reply:

"I don't have enough information from the provided documents."

Do not make up facts.
"""

    def build(
        self,
        question: str,
        context: str,
    ) -> str:

        prompt = f"""
{self.SYSTEM_PROMPT}

------------------------------

Context

{context}

------------------------------

Question

{question}

------------------------------

Answer:
"""

        return prompt