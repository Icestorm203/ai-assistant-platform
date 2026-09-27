import aiohttp

from app.core.config import settings
from app.llm.models import FALLBACK_MODELS

import app.llm.runtime_config as runtime_config
from app.llm.tools import TOOLS_DESCRIPTION

class OpenRouterClient:

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    async def ask(self, prompt: str) -> str:

        headers = {
            "Authorization": (
                f"Bearer {settings.openrouter_api_key}"
            ),
            "Content-Type": "application/json"
        }

        models = [
            runtime_config.current_model,
            *[
                model
                for model in FALLBACK_MODELS
                if model != runtime_config.current_model
            ]
        ]

        last_error = None

        async with aiohttp.ClientSession() as session:

            for model in models:

                payload = {
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": TOOLS_DESCRIPTION
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }

                try:

                    async with session.post(
                        self.BASE_URL,
                        headers=headers,
                        json=payload
                    ) as response:

                        print(
                            f"MODEL={model} "
                            f"STATUS={response.status}"
                        )

                        if response.status != 200:

                            error_text = (
                                await response.text()
                            )

                            last_error = (
                                f"{model}: "
                                f"{response.status}"
                            )

                            print(error_text)

                            continue

                        data = await response.json()

                        answer = (
                            data["choices"][0]
                            ["message"]
                            ["content"]
                        )
                        
                        runtime_config.last_success_model = model

                        return answer

                except Exception as e:

                    last_error = (
                        f"{model}: {str(e)}"
                    )

                    continue

        raise Exception(
            f"Все модели недоступны.\n"
            f"Последняя ошибка: {last_error}"
        )

    async def get_models(self):

        headers = {
            "Authorization": (
                f"Bearer {settings.openrouter_api_key}"
            )
        }

        async with aiohttp.ClientSession() as session:

            async with session.get(
                "https://openrouter.ai/api/v1/models?limit=500",
                headers=headers
            ) as response:

                response.raise_for_status()

                return await response.json()