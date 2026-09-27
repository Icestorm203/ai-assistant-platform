from app.llm.openrouter_client import OpenRouterClient


def test_client_creation():

    client = OpenRouterClient()

    assert client is not None