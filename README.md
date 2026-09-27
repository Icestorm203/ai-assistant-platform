# AI Assistant Platform

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Docker](https://img.shields.io/badge/Docker-Supported-blue)
![Pytest](https://img.shields.io/badge/Tests-5%20passed-success)

Платформа ИИ-ассистента на Python, объединяющая:

- FastAPI API для внешних интеграций
- Telegram-бота на aiogram
- LLM-агента через OpenRouter
- Redis-кеширование и Celery-фоновые задачи
- интеграции с OpenWeatherMap и GitHub API

Проект предназначен для экспериментов с AI-агентом, который может отвечать на вопросы, вызывать инструменты и выдавать данные о погоде и статистике GitHub пользователя.

## Что умеет проект

- Получать текущую погоду по городу через FastAPI
- Собирать базовую информацию и статистику GitHub по пользователю
- Запускать асинхронного AI-агента с поддержкой инструментов
- работать через Telegram-команды:
  - /start
  - /weather <город>
  - /ask <вопрос>
  - /model
  - /setmodel <model_name>
  - /models
- Использовать Redis для кэширования запросов
- Выполнять фоновые задачи через Celery

## Функции

✅ FastAPI Backend

✅ Telegram Bot (Aiogram)

✅ OpenRouter LLM Integration

✅ Function Calling

✅ Weather API Integration

✅ GitHub API Integration

✅ Redis Caching

✅ Celery Background Tasks

✅ Docker Compose Deployment

✅ Pytest Test Suite

✅ GitHub Actions CI

## Архитектура

Проект состоит из нескольких независимых модулей:

- app/main.py — точка входа FastAPI
- app/run_bot.py — запуск Telegram-бота
- app/api/ — HTTP-эндпоинты
- app/services/ — бизнес-логика
- app/clients/ — клиенты внешних API
- app/cache/ — Redis client
- app/tasks/ — Celery задачи
- app/telegram/ — обработчики бота
- app/llm/ — LLM-агент, модели и инструменты
- app/core/ — конфигурация
- app/schemas/ — Pydantic модели

## Технологии

- Python 3.12
- FastAPI
- aiogram
- Celery
- Redis
- aiohttp
- Pydantic v2
- pytest
- Docker / Docker Compose

## Структура проекта

```text
ai-assistant-platform/
├── app/
│   ├── api/
│   │   ├── github.py
│   │   ├── health.py
│   │   ├── tasks.py
│   │   └── weather.py
│   ├── cache/
│   │   └── redis_client.py
│   ├── clients/
│   │   ├── github_client.py
│   │   └── weather_client.py
│   ├── core/
│   │   ├── config.py
│   │   └── http_client.py
│   ├── llm/
│   │   ├── agent.py
│   │   ├── models.py
│   │   ├── openrouter_client.py
│   │   ├── runtime_config.py
│   │   └── tools.py
│   ├── schemas/
│   │   ├── github.py
│   │   └── weather.py
│   ├── services/
│   │   ├── github_service.py
│   │   └── weather_service.py
│   ├── tasks/
│   │   ├── celery_app.py
│   │   └── report_tasks.py
│   ├── telegram/
│   │   ├── bot.py
│   │   └── handlers.py
│   ├── main.py
│   └── run_bot.py
├── tests/
│   ├── test_celery.py
│   ├── test_github_stats.py
│   ├── test_health.py
│   ├── test_openrouter_client.py
│   └── test_weather_api.py
├── .env.example 
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
├── README.md
└── ...
```

## Требования

Перед запуском убедитесь, что у вас установлены:

- Python 3.12+
- Docker и Docker Compose (опционально, если запускаете через контейнеры)
- Redis
- Аккаунт и API-ключи:
  - OpenWeatherMap
  - Telegram Bot Token
  - OpenRouter API Key

## Конфигурация окружения

Создайте файл `.env` в корне проекта со следующими переменными:

```env
weather_api_key=your_openweather_api_key
telegram_bot_token=your_telegram_bot_token
openrouter_api_key=your_openrouter_key
default_llm_model=nvidia/nemotron-3-super-120b-a12b:free
redis_host=localhost
redis_port=6379
```

> Важно: `default_llm_model` используется как основная модель LLM, а при проблемах с доступностью агент переключается на резервные модели из `app/llm/models.py`.

## Запуск локально

### 1. Установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# или
.venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. Запуск Redis

Если Redis не запущен локально:

```bash
redis-server
```

### 3. Запуск API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Запуск Telegram-бота

```bash
python -m app.run_bot
```

### 5. Запуск Celery worker

```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

## Запуск через Docker Compose

В корне проекта есть `docker-compose.yml`:

```bash
docker compose up --build
```

Это запускает:

- Redis
- API
- Telegram bot
- Celery worker

## API

### Health

```http
GET /health
```

Ответ:

```json
{
  "status": "ok"
}
```

### Погода

```http
GET /weather/{city}
```

Пример:

```bash
curl http://localhost:8000/weather/Moscow
```

Ответ:

```json
{
  "city": "Moscow",
  "temperature": 18.7,
  "humidity": 55,
  "description": "пасмурно"
}
```

### GitHub

```http
GET /github/{username}
GET /github/full/{username}
GET /github/stats/{username}
```

Пример:

```bash
curl http://localhost:8000/github/stats/octocat
```

### Задачи Celery

```http
POST /tasks/github-report/{username}
GET /tasks/{task_id}
```

Пример:

```bash
curl -X POST http://localhost:8000/tasks/github-report/octocat
```

## Telegram команды

### /start

Приветствие и запуск бота.

### /weather <город>

Показывает погоду в городе через API приложения.

Пример:

```text
/weather Moscow
```

### /ask <вопрос>

Отправляет запрос в LLM с поддержкой встроенных инструментов. Агент может выбрать один из инструментов:

- weather
- github_stats

Если запрос не требует инструментов, возвращает обычный текстовый ответ.

Пример:

```text
/ask Какая погода в Санкт-Петербурге?
/ask Сколько репозиториев у пользователя octocat и какие языки там используются?
```

### /model

Показывает текущую модель LLM.

### /setmodel <model_name>

Меняет активную модель для текущей сессии/использования.

### /models

Показывает доступные fallback-модели.

## Пример работы AI-агента

LLM получает промпт и должен возвращать JSON в одном из форматов:

```json
{
  "tool": "weather",
  "city": "Moscow"
}
```

или

```json
{
  "tool": "github_stats",
  "username": "octocat"
}
```

или обычный ответ:

```json
{
  "tool": null,
  "answer": "Привет! Чем могу помочь?"
}
```

## Кэширование

Используется Redis для хранения результатов запросов:

- погода по городу
- статистика GitHub по пользователю

Кэш живет 60 секунд для этих сущностей.

## Тестирование

Проект содержит тесты для проверки основного поведения:

Пример запуска:

```bash
pytest
```

Результат:

```text
5 passed
```

Основные проверки покрывают:

- health endpoint
- OpenRouter client behavior
- weather API
- GitHub stats
- Celery task execution

## CI/CD

Для проекта настроен GitHub Actions.

При каждом push автоматически выполняется:

```bash
pytest
```

Workflow расположен в:

```text
.github/workflows/tests.yml
```

## Примечания

- В текущем состоянии проект является учебным/экспериментальным AI-проектом.
- Все LLM-запросы зависят от доступности внешних API и ключей в `.env`.
- Для production-среды потребуется:
  - безопасное хранение секретов
  - rate limiting
  - логирование и мониторинг
  - обработка ошибок внешних API
  - более строгая структура конфигурации

## Возможные улучшения

- добавление авторизации и пользователей
- хранение диалогов в базе данных
- разделение ролей сервисов и очередей
- поддержка нескольких интеграций AI-инструментов
- веб-интерфейс для управления администратором
- более богатая модель работы с GitHub API

## Разработка

Для локальной разработки и отладки удобно использовать:

```bash
pytest
python -m app.run_bot
uvicorn app.main:app --reload
```

## Продемонстрированные навыки

- Python
- FastAPI
- Asyncio
- REST API
- Redis
- Celery
- Docker
- Docker Compose
- Aiogram
- OpenRouter API
- Function Calling
- External API Integration
- Pytest
- GitHub Actions