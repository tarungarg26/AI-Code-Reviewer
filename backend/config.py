import os
from dotenv import load_dotenv

load_dotenv()

CODER_API_KEY = os.getenv("CODER_API_KEY") or os.getenv("OPENROUTER_API_KEY", "")
CRITIC_API_KEY = os.getenv("CRITIC_API_KEY") or os.getenv("OPENROUTER_API_KEY", "")

def _detect_base_url_and_model(api_key: str):
    """Auto-detect base URL and fallback model based on key format."""
    base_url = None
    model = "openrouter/auto"

    if api_key:
        if api_key.startswith("sk-or-"):
            base_url = "https://openrouter.ai/api/v1"
            model = "openrouter/auto"
        elif api_key.startswith("AQ.") or api_key.startswith("AIza"):
            base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
            model = "gemini-2.5-flash"
        elif api_key.startswith("sk-"):
            base_url = None
            model = "gpt-4o-mini"

    return base_url, model

_coder_base, _coder_model = _detect_base_url_and_model(CODER_API_KEY)
_critic_base, _critic_model = _detect_base_url_and_model(CRITIC_API_KEY)

CODER_BASE_URL = os.getenv("CODER_BASE_URL", _coder_base)
CRITIC_BASE_URL = os.getenv("CRITIC_BASE_URL", _critic_base)

CODER_MODEL = os.getenv("CODER_MODEL", _coder_model)
CRITIC_MODEL = os.getenv("CRITIC_MODEL", _critic_model)