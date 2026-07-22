from functools import lru_cache

from anthropic import Anthropic

from app.core.config import settings

EXPANSION_SYSTEM_PROMPT = (
    "You expand a vague, fuzzy description of remembered video content into a "
    "short, keyword-rich search query. The user is trying to find a video they "
    "watched based on a fragmentary memory (a visual, a sound, a phrase, a "
    "vibe). Rewrite it into a dense list of likely synonyms, related concepts, "
    "and descriptive keywords that might appear in a transcript or on-screen "
    "text. Respond with ONLY the expanded query text, no explanation."
)


@lru_cache(maxsize=1)
def _get_client() -> Anthropic:
    return Anthropic(api_key=settings.anthropic_api_key)


def expand_query(query: str) -> str:
    if not settings.anthropic_api_key.strip():
        return query

    client = _get_client()
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=256,
        system=EXPANSION_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": query}],
    )
    text = "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()
    return text or query
