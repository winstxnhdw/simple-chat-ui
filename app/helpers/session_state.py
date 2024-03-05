from streamlit import session_state

from app.types import SessionState

SESSION_STATE: SessionState = session_state  # type: ignore
