from pydantic import BaseModel, Field, field_validator


class CodeRequest(BaseModel):
    problem: str = Field(..., description="Programming problem description")

    @field_validator("problem")
    @classmethod
    def validate_problem_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Problem statement cannot be empty.")
        return v.strip()