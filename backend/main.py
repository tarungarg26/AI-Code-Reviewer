import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from .models import CodeRequest
from .coder import generate_code
from .critic import review_code
from .comparison import compare_code

app = FastAPI(
    title="CodeLoop AI",
    description="AI Coder and AI Critic system",
    version="1.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_INDEX = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "frontend",
    "index.html"
)


@app.get("/")
def home():
    if os.path.exists(FRONTEND_INDEX):
        return FileResponse(FRONTEND_INDEX)
    return {"message": "CodeLoop AI is running"}


@app.get("/api/status")
def status():
    return {
        "message": "CodeLoop AI is running"
    }


@app.post("/review")
def review(request: CodeRequest):
    try:
        code_v1 = generate_code(request.problem)

        criticism = review_code(
            request.problem,
            code_v1
        )

        code_v2 = generate_code(
            request.problem,
            code_v1,
            criticism
        )

        comparison = compare_code(
            code_v1,
            code_v2
        )

        return {
            "code_v1": code_v1,
            "critic_review": criticism,
            "code_v2": code_v2,
            "comparison": comparison
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in review pipeline: {str(e)}"
        )