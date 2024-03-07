from streamlit import markdown

from app.api import Examplify
from app.components import render_chat, render_sidebar
from app.helpers import SESSION_STATE


def run():
    """
    Summary
    -------
    the Streamlit entrypoint
    """
    markdown('<style>header { visibility: hidden; }</style>', unsafe_allow_html=True)

    if 'chats' not in SESSION_STATE:
        SESSION_STATE['chats'] = { 1: [] }

    if 'current_chat' not in SESSION_STATE:
        SESSION_STATE['current_chat'] = 1

    with Examplify('https://localhost/api') as api:
        render_chat(api)
        render_sidebar(api)
