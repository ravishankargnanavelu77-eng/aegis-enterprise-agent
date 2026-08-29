import time
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings


def get_llm():
    """Create and return the configured Gemini LLM."""

    settings = get_settings()

    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_api_key,
    )


def invoke_with_retry(
    runnable: Any,
    prompt: str,
    max_retries: int = 5,
    base_delay: int = 15,
):
    """
    Invoke any LangChain runnable with exponential-backoff retry.

    Works with:
    - Normal LLM calls
    - Structured output LLMs
    - Future LangChain runnables
    """

    last_error = None

    for attempt in range(max_retries):
        try:
            return runnable.invoke(prompt)

        except Exception as error:
            last_error = error

            error_message = str(error).lower()

            is_retryable = (
                "429" in error_message
                or "resource_exhausted" in error_message
                or "rate limit" in error_message
                or "quota" in error_message
                or "temporarily unavailable" in error_message
                or "503" in error_message
                or "500" in error_message
            )

            if not is_retryable:
                raise

            if attempt == max_retries - 1:
                break

            delay = base_delay * (2 ** attempt)

            print(
                f"\n[LLM RETRY] Temporary API limit/error detected."
                f" Attempt {attempt + 1}/{max_retries}."
                f" Retrying in {delay} seconds..."
            )

            time.sleep(delay)

    raise last_error
