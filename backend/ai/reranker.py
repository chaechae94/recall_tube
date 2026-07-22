import json

from anthropic import Anthropic

from app.core.config import settings

RERANK_SYSTEM_PROMPT = (
    "You help find a video the user vaguely remembers. You will be given the "
    "user's memory description and a list of candidate video moments (with "
    "their spoken/on-screen text). For each candidate, write ONE short "
    "sentence in Korean explaining why it might (or might not) match the "
    "user's memory. Then order every candidate from most to least likely "
    "match, with no ties."
)

RERANK_SCHEMA = {
    "type": "object",
    "properties": {
        "ranked": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer"},
                    "reason": {"type": "string"},
                },
                "required": ["index", "reason"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["ranked"],
    "additionalProperties": False,
}


def rerank_with_reasons(query: str, candidates: list[dict]) -> list[dict]:
    if not candidates or not settings.anthropic_api_key.strip():
        return [{**candidate, "reason": ""} for candidate in candidates]

    client = Anthropic(api_key=settings.anthropic_api_key)
    candidate_lines = "\n".join(
        f"{i}. speech: {c['speech_text'] or '(none)'} | on-screen text: {c['ocr_text'] or '(none)'}"
        for i, c in enumerate(candidates)
    )
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=RERANK_SYSTEM_PROMPT,
        output_config={"format": {"type": "json_schema", "schema": RERANK_SCHEMA}},
        messages=[
            {
                "role": "user",
                "content": f"User's memory: {query}\n\nCandidates:\n{candidate_lines}",
            }
        ],
    )
    text = "".join(block.text for block in response.content if block.type == "text")
    parsed = json.loads(text)

    reason_by_index = {item["index"]: item["reason"] for item in parsed["ranked"]}
    order = [item["index"] for item in parsed["ranked"]]

    reranked = [
        {**candidates[idx], "reason": reason_by_index.get(idx, "")}
        for idx in order
        if 0 <= idx < len(candidates)
    ]
    seen = set(order)
    reranked.extend(
        {**c, "reason": ""} for i, c in enumerate(candidates) if i not in seen
    )
    return reranked
