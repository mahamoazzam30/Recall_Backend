import httpx

from app.config import get_settings


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts via the configured embedding provider.

    Returns one vector per input text, in order.
    """
    settings = get_settings()
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
    }
    payload = {"model": settings.embedding_model, "input": texts}

    async with httpx.AsyncClient(base_url=settings.openrouter_base_url, timeout=30) as client:
        resp = await client.post("/embeddings", headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

    return [item["embedding"] for item in data["data"]]


async def embed_text(text: str) -> list[float]:
    vectors = await embed_texts([text])
    return vectors[0]
