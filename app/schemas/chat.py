from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ChatSourceOut(BaseModel):
    content: str
    page_ref: str | None


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSourceOut]
