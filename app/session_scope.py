import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Optional

_session_context: ContextVar[str] = ContextVar("session_context")


@contextmanager
def set_scoped_context(session_id: Optional[str] = None) -> None:
    _session_id: str = session_id or str(uuid.uuid4())
    token = _session_context.set(_session_id)
    try:
        yield
    finally:
        _session_context.reset(token)


def get_session_context() -> str:
    return _session_context.get()

