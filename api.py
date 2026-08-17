from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent.router import LogicAgent

app = FastAPI(title="Logic Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = None


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="请输入需要分析的陈述。")

    global agent
    try:
        if agent is None:
            agent = LogicAgent()
        return agent.run(text)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"分析失败：{type(exc).__name__}: {exc}",
        ) from exc
