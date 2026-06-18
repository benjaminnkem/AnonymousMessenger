from pydantic import BaseModel, Field


class MessageDto(BaseModel):
    content: str
    public_id: str
    role: str
