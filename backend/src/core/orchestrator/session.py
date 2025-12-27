import asyncio
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.models.orchestrator import OrchestratorConfig


class ChatMessage(BaseModel):
    role: str = Field(..., description="user, assistant, or system")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SessionContext:
    def __init__(self, session_id: Optional[UUID] = None):
        self.session_id: UUID = session_id or uuid4()
        self.history: List[ChatMessage] = []
        self.current_task: Optional[asyncio.Task] = None
        self.config: OrchestratorConfig = OrchestratorConfig()

    def add_message(self, role: str, content: str):
        self.history.append(ChatMessage(role=role, content=content))

    def clear_history(self):
        self.history = []

    def cancel_current_task(self):
        if self.current_task and not self.current_task.done():
            self.current_task.cancel()
            self.current_task = None
