# CodeLoop AI - Project Context & Architecture

## 1. Project Overview

**CodeLoop AI (AI Code Reviewer)** is an automated, multi-agent code generation, review, and refinement system. It pairs a **Coder AI** with a **Critic AI** in a continuous feedback loop:
1. The **Coder AI** receives a problem description and produces an initial solution (`code_v1`).
2. The **Critic AI** analyzes `code_v1` against 8 strict criteria (correctness, edge cases, time/space complexity, etc.) and provides actionable feedback.
3. The **Coder AI** receives the critic's feedback along with the initial code and generates an improved solution (`code_v2`).
4. A **Comparison Engine** calculates quantitative metrics between `code_v1` and `code_v2` (line, character, and word count deltas, and percentage change).

The system can be used through:
- **Interactive Web Interface**: Single-page application served directly by FastAPI.
- **Terminal CLI**: Interactive command-line tool (`cli.py`).
- **REST API**: Standard JSON endpoints (`POST /review`).

---

## 2. Architecture & Execution Flow

```
                  +-------------------------+
                  |  User Input (Problem)   |
                  +------------+------------+
                               |
                               v
                  +-------------------------+
                  |     Coder Agent         |  --> Generates code_v1
                  +------------+------------+
                               |
                               v
                  +-------------------------+
                  |     Critic Agent        |  --> Evaluates code_v1 (8 criteria)
                  +------------+------------+
                               |
                               v
                  +-------------------------+
                  |     Coder Agent         |  --> Refines code based on feedback
                  +------------+------------+      (Produces code_v2)
                               |
                               v
                  +-------------------------+
                  |    Comparison Engine    |  --> Computes diff metrics
                  +------------+------------+
                               |
                               v
                  +-------------------------+
                  |  Response / UI Render   |
                  +-------------------------+
```

---

## 3. Project Directory Structure

```
d:/AI Code Reviewer/
|-- backend/
|   |-- __init__.py
|   |-- config.py         # Environment variables & dynamic provider detection
|   |-- models.py         # Pydantic data models & request validation
|   |-- coder.py          # Coder agent prompt and execution logic
|   |-- critic.py         # Critic agent review prompt and execution logic
|   |-- comparison.py     # Difference and metrics calculation between v1 and v2
|   `-- main.py           # FastAPI application, CORS, endpoints, and UI hosting
|-- frontend/
|   `-- index.html        # Responsive web UI (Tailwind CSS, Highlight.js, Marked.js)
|-- venv/                 # Python virtual environment
|-- .env                  # API keys and environment configuration
|-- cli.py                # Command-line interface for terminal usage
|-- requirements.txt      # Python dependencies
`-- context.md            # Complete project documentation & context
```

---

## 4. Module Breakdown

### `backend/config.py`
Manages API keys, model names, and base URLs. Features automatic provider detection:
- **OpenRouter (`sk-or-...`)**: Routes to `https://openrouter.ai/api/v1` with default model `openrouter/auto`.
- **Google Gemini (`AQ...` or `AIza...`)**: Routes to Google's OpenAI-compatible endpoint `https://generativelanguage.googleapis.com/v1beta/openai/` with model `gemini-2.5-flash`.
- **OpenAI (`sk-...`)**: Routes to standard OpenAI API with model `gpt-4o-mini`.
- Allows manual overrides via environment variables: `CODER_MODEL`, `CRITIC_MODEL`, `CODER_BASE_URL`, `CRITIC_BASE_URL`.

### `backend/models.py`
Defines the Pydantic schemas:
- `CodeRequest`: Input payload with automatic string stripping and validation preventing empty/whitespace-only problem descriptions.

### `backend/coder.py`
Implements `generate_code(problem, previous_code=None, review=None)`:
- In initial mode: Solves the problem from scratch without explanatory text.
- In refinement mode: Takes the original code and the critic's feedback to produce an improved, robust version.
- Includes OpenRouter headers (`HTTP-Referer`, `X-Title`) when targeting OpenRouter.

### `backend/critic.py`
Implements `review_code(problem, code)`:
- Evaluates code against:
  1. Correctness
  2. Logical errors
  3. Edge cases
  4. Time complexity
  5. Space complexity
  6. Unnecessary code
  7. Readability
  8. Actionable improvements
- Instructed not to write the full solution directly, but to guide the Coder AI.

### `backend/comparison.py`
Implements `compare_code(code1, code2)`:
- Calculates character, line, and word count deltas.
- Computes `character_change_percent`.
- Safely handles null/empty string inputs.

### `backend/main.py`
FastAPI application defining:
- `GET /`: Serves the interactive `frontend/index.html`.
- `GET /api/status`: Health check endpoint.
- `POST /review`: Orchestrates the full review pipeline and returns structured JSON.
- `CORSMiddleware`: Permits requests from external frontends / localhost ports.
- Exception handling returning structured HTTP errors.

### `frontend/index.html`
A single-page web app built with Tailwind CSS, Highlight.js, and Marked.js:
- Large multiline input area with keyboard shortcut (`Ctrl + Enter`).
- Quick sample problems (Two Sum, LRU Cache, Valid Parentheses).
- Loading status indicator for multi-agent pipeline.
- Side-by-side comparison cards for `code_v1` and `code_v2` with syntax highlighting and copy buttons.
- Markdown rendering for critic feedback.
- Difference metrics banner (lines, characters, words, percentage change).

### `cli.py`
Terminal interface allowing users to input problem statements, observe each agent's output sequentially, and inspect metrics without starting a browser.

---

## 5. API Reference

### `GET /`
Serves the web application user interface (`text/html`).

### `GET /api/status`
Health check endpoint.
- **Response**: `200 OK`
```json
{
  "message": "CodeLoop AI is running"
}
```

### `POST /review`
Main code generation and critique pipeline.
- **Headers**: `Content-Type: application/json`
- **Request Body**:
```json
{
  "problem": "Write a Python function to check if a number is prime."
}
```
- **Response (`200 OK`)**:
```json
{
  "code_v1": "def is_prime(n):\n    ...",
  "critic_review": "### Correctness\nThe submitted code is correct...",
  "code_v2": "import math\n\ndef is_prime(n):\n    ...",
  "comparison": {
    "version_1": {"characters": 290, "lines": 15, "words": 61},
    "version_2": {"characters": 329, "lines": 18, "words": 64},
    "difference": {"characters": 39, "lines": 3, "words": 3},
    "character_change_percent": 13.45
  }
}
```

---

## 6. Environment Configuration (`.env`)

```env
# Primary API Keys (supports OpenRouter, Google Gemini, or OpenAI)
CODER_API_KEY=sk-or-v1-...
CRITIC_API_KEY=sk-or-v1-...

# Optional: Shared fallback key for OpenRouter
# OPENROUTER_API_KEY=sk-or-v1-...

# Optional: Model overrides (default auto-detected from key)
# CODER_MODEL=openrouter/auto
# CRITIC_MODEL=openrouter/auto

# Optional: Base URL overrides
# CODER_BASE_URL=https://openrouter.ai/api/v1
# CRITIC_BASE_URL=https://openrouter.ai/api/v1
```

---

## 7. How to Run

### Installation
Activate virtual environment and install dependencies:
```powershell
.\venv\Scripts\pip install -r requirements.txt
```

### 1. Web Application (Recommended)
Start the FastAPI server:
```powershell
.\venv\Scripts\uvicorn backend.main:app --reload
```
Open **http://localhost:8000** in your browser.

### 2. Interactive Terminal CLI
Run the CLI script:
```powershell
.\venv\Scripts\python cli.py
```

### 3. API Documentation
Swagger UI documentation is available at **http://localhost:8000/docs**.
