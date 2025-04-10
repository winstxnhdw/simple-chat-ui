from streamlit import markdown, session_state

from app.api import Examplify
from app.components import render_chat, render_sidebar
from app.types import SessionState


def run() -> None:
    """
    Summary
    -------
    the Streamlit entrypoint
    """
    markdown("<style>header { visibility: hidden; }</style>", unsafe_allow_html=True)
    state: SessionState = session_state  # pyright: ignore [reportAssignmentType]

    if "chats" not in state:
        state["chats"] = {1: []}

    if "current_chat" not in state:
        state["current_chat"] = 1

    if "store_query" not in state:
        state["store_query"] = True

    if "search_size" not in state:
        state["search_size"] = 0

    with Examplify("https://localhost/api") as api:
        render_chat(api, state)
        render_sidebar(api, state)
