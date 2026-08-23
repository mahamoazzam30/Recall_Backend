import json
import re

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import get_settings
from app.llm.prompt_log import log_call

_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)

# Free OpenRouter models get rate-limited on the shared pool unpredictably.
# settings.openrouter_model is tried first; these back it up so a single
# busy model doesn't take question-generation down mid-session.
_FALLBACK_FREE_MODELS = [
    "nvidia/nemotron-nano-9b-v2:free",
    "liquid/lfm-2.5-2.6b:free",
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
]


def _parse_json_loosely(content: str) -> dict:
    """Parse a JSON object out of a model response.

    `response_format: json_object` is a hint, not a guarantee — some
    OpenRouter-hosted models (especially free ones) ignore it and wrap the
    object in prose or code fences. Fall back to extracting the first
    {...} block before giving up.
    """
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    match = _JSON_OBJECT_RE.search(content)
    if match is None:
        raise json.JSONDecodeError("no JSON object found in model response", content, 0)
    return json.loads(match.group(0))


class OpenRouterClient:
    """Thin wrapper around the OpenRouter chat-completions API.

    Used for question generation and course chat. Retries with exponential
    backoff and falls back across a pool of free models if the configured
    one is rate-limited.
    """

    def __init__(self) -> None:
        self._settings = get_settings()
        primary = self._settings.openrouter_model
        self._models = [primary] + [m for m in _FALLBACK_FREE_MODELS if m != primary]

    async def complete_json(self, system_prompt: str, user_prompt: str, call_site: str) -> dict:
        content = await self.complete(system_prompt, user_prompt, call_site, json_mode=True)
        return _parse_json_loosely(content)

    async def complete(
        self, system_prompt: str, user_prompt: str, call_site: str, json_mode: bool = False
    ) -> str:
        last_error: Exception | None = None
        for model in self._models:
            try:
                return await self._complete_with_model(model, system_prompt, user_prompt, call_site, json_mode)
            except Exception as exc:
                last_error = exc
                continue
        raise last_error or RuntimeError("no OpenRouter model available")

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=1, max=4))
    async def _complete_with_model(
        self, model: str, system_prompt: str, user_prompt: str, call_site: str, json_mode: bool
    ) -> str:
        settings = self._settings
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        async with httpx.AsyncClient(base_url=settings.openrouter_base_url, timeout=30) as client:
            resp = await client.post("/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()

        content = data["choices"][0]["message"]["content"]
        log_call(call_site, f"[{model}] {system_prompt}\n\n{user_prompt}", content)
        return content
