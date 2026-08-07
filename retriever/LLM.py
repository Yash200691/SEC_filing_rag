"""
LLM interface for Grok.
"""

from openai import OpenAI

from config import settings


class GrokLLM:
    """
    Handles communication with the Grok API.
    """

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.XAI_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )

        self.model = settings.GROK_MODEL

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate an answer using Grok.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content