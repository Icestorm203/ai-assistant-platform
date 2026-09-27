import aiohttp


class HTTPClient:
    session: aiohttp.ClientSession | None = None


http_client = HTTPClient()