import aiohttp

from aiogram import Router
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import Message

import app.llm.runtime_config as runtime_config
from app.core.config import settings
from app.llm.models import FALLBACK_MODELS
from app.llm.agent import Agent

agent = Agent()

router = Router()

API_BASE = settings.api_base_url


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Привет! Я AI Assistant Platform Bot"
    )


@router.message(Command("weather"))
async def weather_handler(message: Message):

    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer(
            "Использование: /weather Moscow"
        )
        return

    city = parts[1]

    async with aiohttp.ClientSession() as session:

        async with session.get(
            f"{API_BASE}/weather/{city}"
        ) as response:

            if response.status != 200:
                await message.answer(
                    f"⚠️ Не удалось получить погоду для «{city}» "
                    f"(код {response.status})"
                )
                return

            data = await response.json()

    await message.answer(
        f"📍 {data['city']}\n"
        f"🌡 Температура: {data['temperature']}°C\n"
        f"💧 Влажность: {data['humidity']}%\n"
        f"☁ {data['description']}"
    )


@router.message(Command("ask"))
async def ask_handler(message: Message):

    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:

        await message.answer(
            "Использование:\n/ask Ваш вопрос"
        )

        return

    prompt = parts[1]

    await message.answer(
        "🤔 Думаю..."
    )

    try:

        result = await agent.process(prompt)
        print(result)

        # Weather Tool
        if result["tool"] == "weather":

            city = result["city"]

            async with aiohttp.ClientSession() as session:

                async with session.get(
                    f"{API_BASE}/weather/{city}"
                ) as response:
                    if response.status != 200:
                        await message.answer(
                            f"⚠️ Не удалось получить погоду для «{city}» "
                            f"(код {response.status})"
                        )
                        return 

                    weather = await response.json()

            await message.answer(
                f"📍 {weather['city']}\n"
                f"🌡 Температура: {weather['temperature']}°C\n"
                f"💧 Влажность: {weather['humidity']}%\n"
                f"☁ {weather['description']}"
            )

            return

        # GitHub Stats Tool
        if result["tool"] == "github_stats":

            username = result["username"]

            async with aiohttp.ClientSession() as session:

                async with session.get(
                    f"{API_BASE}/github/stats/{username}"
                ) as response:
                    if response.status != 200:
                        await message.answer(
                            f"⚠️ Не удалось получить статистику GitHub "
                            f"для «{username}» (код {response.status})"
                        )
                        return 

                    stats = await response.json()

            languages = "\n".join(
                f"• {lang}: {count}"
                for lang, count in stats["languages"].items()
            )

            await message.answer(
                f"👤 Пользователь: {username}\n"
                f"📦 Репозиториев: {stats['total_repositories']}\n\n"
                f"🔤 Языки:\n{languages}"
            )

            return

        # Обычный ответ

        await message.answer(
            result["answer"]
        )

    except Exception as e:

        await message.answer(
            f"Ошибка LLM API:\n{e}"
        )


@router.message(Command("model"))
async def model_handler(message: Message):

    text = (
        f"Текущая модель:\n"
        f"{runtime_config.current_model}"
    )

    if runtime_config.last_success_model:

        text += (
            "\n\nПоследняя успешная модель:\n"
            f"{runtime_config.last_success_model}"
        )

    await message.answer(text)


@router.message(Command("setmodel"))
async def set_model_handler(message: Message):

    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:

        await message.answer(
            "Использование:\n"
            "/setmodel model_name"
        )

        return

    runtime_config.current_model = parts[1]

    await message.answer(
        f"✅ Модель изменена:\n"
        f"{runtime_config.current_model}"
    )


@router.message(Command("models"))
async def models_handler(message: Message):

    await message.answer(
        "\n".join(FALLBACK_MODELS)
    )