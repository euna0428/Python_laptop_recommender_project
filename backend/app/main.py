from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .recommender import load_departments, load_laptops, department_to_dict, laptop_to_dict, recommend


class MemberInput(BaseModel):
    name: str = Field(default="", description="사용자 이름 또는 닉네임")
    studentId: str = Field(default="", description="학번 또는 구분값")
    grade: str = Field(default="", description="학년")


class RecommendRequest(BaseModel):
    member: MemberInput = Field(default_factory=MemberInput)
    department: str
    budget: int = Field(ge=300000, le=6000000)
    priorities: list[Literal["price", "performance", "weight"]] = ["price"]
    os: Literal["windows", "macos", "freedos", "any"] = "any"
    canInstallWindows: bool = False
    limit: int = Field(default=5, ge=1, le=10)


app = FastAPI(
    title="학과별 노트북 추천 API",
    description="기존 CLI 추천 로직을 React 웹 페이지에서 사용할 수 있도록 REST API로 전환한 백엔드입니다.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/departments")
def departments() -> dict[str, list[dict]]:
    df = load_departments()
    return {"departments": [department_to_dict(row, idx) for idx, row in df.iterrows()]}


@app.get("/api/laptops")
def laptops() -> dict[str, list[dict]]:
    df = load_laptops()
    return {"laptops": [laptop_to_dict(row) for _, row in df.iterrows()]}


@app.post("/api/recommend")
def create_recommendation(request: RecommendRequest) -> dict:
    try:
        return recommend(request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
