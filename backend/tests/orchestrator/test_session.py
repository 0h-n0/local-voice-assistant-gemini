import asyncio
import pytest
from src.core.orchestrator.session import SessionContext


def test_session_history():
    session = SessionContext()
    assert len(session.history) == 0
    
    session.add_message("user", "Hello")
    session.add_message("assistant", "Hi there!")
    
    assert len(session.history) == 2
    assert session.history[0].role == "user"
    assert session.history[1].role == "assistant"
    
    session.clear_history()
    assert len(session.history) == 0

@pytest.mark.asyncio
async def test_session_task_cancellation():
    session = SessionContext()
    
    async def dummy_task():
        await asyncio.sleep(10)
        
    task = asyncio.create_task(dummy_task())
    session.current_task = task
    
    session.cancel_current_task()
    try:
        await task
    except asyncio.CancelledError:
        pass
    assert task.cancelled()
