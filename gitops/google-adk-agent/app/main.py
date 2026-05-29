import os
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from pydantic import BaseModel, Field

from agent import root_agent


APP_NAME = os.getenv("APP_NAME", "google-adk-agent")

app = FastAPI(title="Google ADK Agent", version="0.1.0")
session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    user_id: str = "default-user"
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    user_id: str
    session_id: str


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
async def root() -> dict[str, Any]:
    return {
        "name": APP_NAME,
        "agent": root_agent.name,
        "model": os.getenv("ADK_MODEL_NAME", "openai/gpt-oss-120b"),
        "endpoints": ["/healthz", "/chat"],
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    session_id = request.session_id or str(uuid.uuid4())

    try:
        await _ensure_session(request.user_id, session_id)
        message = Content(role="user", parts=[Part(text=request.message)])

        final_parts: list[str] = []
        async for event in runner.run_async(
            user_id=request.user_id,
            session_id=session_id,
            new_message=message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_parts.extend(
                    part.text
                    for part in event.content.parts
                    if getattr(part, "text", None)
                )

        response = "\n".join(final_parts).strip()
        if not response:
            response = "The agent completed without returning text."

        return ChatResponse(
            response=response,
            user_id=request.user_id,
            session_id=session_id,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def _ensure_session(user_id: str, session_id: str) -> None:
    try:
        existing_session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )
        if existing_session:
            return
    except Exception:
        pass

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )
