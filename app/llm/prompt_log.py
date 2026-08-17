"""Append-only log of every LLM call, per the program's transparency requirement.

Every call site (generation, grading, adjudication) must log its prompt and a
truncated response here so `prompts.md` stays a running record of what was
actually sent to the models.
"""
from datetime import datetime, timezone
from pathlib import Path

_LOG_PATH = Path(__file__).resolve().parents[2] / "prompts.md"
_MAX_RESPONSE_CHARS = 800


def log_call(call_site: str, prompt: str, response: str) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    truncated_response = response if len(response) <= _MAX_RESPONSE_CHARS else response[:_MAX_RESPONSE_CHARS] + "…"

    entry = (
        f"\n## [{call_site}] {timestamp}\n\n"
        f"**Prompt:**\n```\n{prompt.strip()}\n```\n\n"
        f"**Response:**\n```\n{truncated_response.strip()}\n```\n"
    )

    with open(_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)
