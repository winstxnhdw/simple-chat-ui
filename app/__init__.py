from streamlit import markdown, session_state

from app.api import Examplify
from app.components import render_chat, render_sidebar
from app.types import SessionState


def run():
    """
    Summary
    -------
    the Streamlit entrypoint
    """
    markdown('<style>header { visibility: hidden; }</style>', unsafe_allow_html=True)
    state: SessionState = session_state  # type: ignore

    if 'chats' not in state:
        state['chats'] = { 1: [] }

    if 'current_chat' not in state:
        state['current_chat'] = 1

    with Examplify('https://localhost/api') as api:
        render_chat(api, state)
        render_sidebar(api, state)
