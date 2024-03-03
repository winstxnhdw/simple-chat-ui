from streamlit import session_state

from app.api import Examplify
from app.components import render_chat, render_sidebar


def main():
    """
    Summary
    -------
    the main function
    """
    if 'chats' not in session_state:
        session_state['chats'] = { 1: [] }

    if 'current_chat' not in session_state:
        session_state['current_chat'] = 1

    with Examplify('https://localhost') as api:
        render_chat(api)
        render_sidebar(api)


if __name__ == '__main__':
    main()
