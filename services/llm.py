from __future__ import annotations

import time

import google.generativeai as genai


class LLMError(RuntimeError):
    pass


def get_gemini_response(
    *,
    prompt: str,
    api_key: str,
    model_id: str,
    timeout_seconds: int = 30,
    max_retries: int = 2,
    temperature: float | None = None,
) -> str:
    """Generate content with lightweight timeout/retry handling."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_id)

    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            generation_config = {"temperature": temperature} if temperature is not None else None
            response = model.generate_content(
                prompt,
                request_options={"timeout": timeout_seconds},
                generation_config=generation_config,
            )
            return (response.text or "").strip()
        except Exception as e:  # noqa: BLE001
            last_error = e
            if attempt < max_retries:
                time.sleep(0.8 * (attempt + 1))
                continue
            break

    raise LLMError(str(last_error) if last_error else "Unknown LLM error")
