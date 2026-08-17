from anthropic import AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import get_settings
from app.llm.prompt_log import log_call


class ClaudeClient:
    """Wrapper around the Anthropic /v1/messages endpoint.

    Used for short-answer grading, contest adjudication, and generating
    miss-explanations — anywhere grading quality matters more than latency
    or cost.
    """

    def __init__(self) -> None:
        self._settings = get_settings()
        self._client = AsyncAnthropic(api_key=self._settings.anthropic_api_key)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
    async def complete(self, system_prompt: str, user_prompt: str, call_site: str) -> str:
        response = await self._client.messages.create(
            model=self._settings.anthropic_model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = "".join(block.text for block in response.content if block.type == "text")
        log_call(call_site, f"{system_prompt}\n\n{user_prompt}", text)
        return text
