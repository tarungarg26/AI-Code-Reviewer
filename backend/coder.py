from openai import OpenAI
from .config import CODER_API_KEY, CODER_BASE_URL, CODER_MODEL

coder_client = OpenAI(
    api_key=CODER_API_KEY,
    base_url=CODER_BASE_URL,
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "CodeLoop AI"
    } if CODER_BASE_URL and "openrouter" in CODER_BASE_URL else None
)

def generate_code(problem: str, previous_code: str = None, review: str = None) -> str:

    prompt = f"""You are the CODER AI.

You are an expert competitive programmer.

Solve the following programming problem.
Write code without comments.

PROBLEM:
{problem}
"""

    if previous_code:
        prompt += f"""

PREVIOUS CODE:
{previous_code}

CRITIC REVIEW:
{review}

Improve the previous code based on the critic's feedback.
"""

    prompt += """

Return only the final code.
Do not explain the code.
"""

    response = coder_client.chat.completions.create(
        model=CODER_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.choices[0].message.content or ""
    return content.strip()