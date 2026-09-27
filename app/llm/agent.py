import json

import aiohttp

from app.llm.openrouter_client import OpenRouterClient

client = OpenRouterClient()


class Agent:

    async def process(
        self,
        prompt: str
    ):

        response = await client.ask(prompt)

        try:

            data = json.loads(response)

            return data

        except Exception:

            return {
                "tool": None,
                "answer": response
            }