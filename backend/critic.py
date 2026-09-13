from openai import OpenAI
from .config import CRITIC_API_KEY, CRITIC_BASE_URL, CRITIC_MODEL

critic_client = OpenAI(
    api_key=CRITIC_API_KEY,
    base_url=CRITIC_BASE_URL,
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "CodeLoop AI"
    } if CRITIC_BASE_URL and "openrouter" in CRITIC_BASE_URL else None
)

def review_code(problem: str, code: str) -> str:

    prompt = f"""You are the CRITIC AI.

You are a strict and experienced programming code reviewer.

Review the submitted code.

Check:

1. Correctness
2. Logical errors
3. Edge cases
4. Time complexity
5. Space complexity
6. Unnecessary code
7. Readability
8. Possible improvements

Write code without comments.

Do NOT write the complete solution.

PROBLEM:
{problem}

CODE:
{code}

Give detailed actionable feedback to the coder.

In the feedback compare both the codes and give pros and cons of both the codes.
"""

    response = critic_client.chat.completions.create(
        model=CRITIC_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.choices[0].message.content or ""
    return content.strip()