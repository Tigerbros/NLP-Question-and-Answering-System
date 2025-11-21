"""Shared utilities for the Q&A CLI and Streamlit app."""

import json
import os
from pathlib import Path
from typing import Dict, Optional
from urllib import error, request

# Load environment variables from a local .env if present.
def _load_local_env(path: Path = Path(".env")) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        normalized = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), normalized)


_load_local_env()

PROMPT_PATH = Path("prompts/qa_prompt.txt")
DEFAULT_MODEL = "x-ai/grok-4.1-fast:free"


def preprocess_question(question: str) -> Dict[str, object]:
    """Lowercase, remove punctuation, and tokenize the question.

    Returns a dictionary containing the normalized question string and a token list.
    """

    stripped = question.strip().lower()
    punctuation = "!?.,;:\"'()[]{}<>/\\|@#$%^&*-_+=~`"
    cleaned_chars = [ch for ch in stripped if ch not in punctuation]
    cleaned_text = "".join(cleaned_chars)
    tokens = cleaned_text.split()
    return {"cleaned": cleaned_text, "tokens": tokens}


def load_prompt_template(path: Path = PROMPT_PATH) -> str:
    """Load the reusable prompt template from disk."""
    return path.read_text(encoding="utf-8")


def build_prompt(question: str) -> str:
    """Fill the prompt template with the provided question."""
    template = load_prompt_template()
    return template.format(question=question)


def _post_json(url: str, payload: Dict[str, object], headers: Dict[str, str]) -> Dict[str, object]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore") if exc.fp else exc.reason
        raise RuntimeError(f"OpenRouter request failed: {exc.code} {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Failed to reach OpenRouter: {exc.reason}") from exc


def send_to_llm(prompt: str, model: str = DEFAULT_MODEL, api_key: Optional[str] = None) -> str:
    """Call OpenRouter's chat completions endpoint and return the first message content."""

    resolved_key = api_key or os.getenv("OPENROUTER_API_KEY") or os.getenv("OPEN_ROUTER_KEY")
    if not resolved_key:
        raise ValueError(
            "OpenRouter API key is required. Set OPENROUTER_API_KEY or pass api_key explicitly."
        )

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }
    headers = {
        "Authorization": f"Bearer {resolved_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/",
        "X-Title": "OpenRouter Q&A Starter",
    }

    data = _post_json("https://openrouter.ai/api/v1/chat/completions", payload, headers)

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected OpenRouter response: {data}") from exc


def run_qa_pipeline(
    question: str, model: str = DEFAULT_MODEL, api_key: Optional[str] = None
) -> Dict[str, object]:
    """End-to-end processing: preprocess, render prompt, and fetch LLM answer."""

    processed = preprocess_question(question)
    prompt = build_prompt(processed["cleaned"])
    answer = send_to_llm(prompt, model=model, api_key=api_key)
    return {"processed": processed, "prompt": prompt, "answer": answer}
