from streamlit import (
    button,
    rerun,
    sidebar,
    title,
)

from app.api import ChatAPI
from app.types import Chats, SessionState


def render_delete_all_button(api: ChatAPI, chats: Chats):
    """
    Summary
    -------
    render the delete all chats button

    Parameters
    ----------
    api (ChatAPI) : the API object
    chats (Chats) : the sequence of chats
    """
    if not button('Delete all', key='delete_all_chats', type='primary', use_container_width=True):
        return

    api.delete_all_chats()
    chats.clear()
    chats[1] = []
    rerun()


def render_add_chat_button(chats: Chats, state: SessionState):
    """
    Summary
    -------
    render the add chat button

    Parameters
    ----------
    chats (Chats) : the sequence of chats
    """
    if not button('＋', key='add_chat', use_container_width=True):
        return

    number_of_chats = len(chats)
    chats[number_of_chats + 1] = []
    state['current_chat'] = number_of_chats
    rerun()


def render_chat_tab(chat: int, state: SessionState):
    """
    Summary
    -------
    render the chat buttons

    Parameters
    ----------
    chat (int) : the current chat identifier
    """
    if not button(str(chat), key=f'chat_tab_{chat}', use_container_width=True):
        return

    state['current_chat'] = chat
    rerun()


def render_tabs(api: ChatAPI, state: SessionState):
    """
    Summary
    -------
    render the chat tabs

    Parameters
    ----------
    api (ChatAPI) : the API object
    """
    chats = state['chats']

    for chat in chats:
        render_chat_tab(chat, state)

    render_add_chat_button(chats, state)
    render_delete_all_button(api, chats)


def render_sidebar(api: ChatAPI, state: SessionState):
    """
    Summary
    -------
    render the chat tabs

    Parameters
    ----------
    api (ChatAPI) : the API object
    """
    with sidebar:
        title('Chats')
        render_tabs(api, state)
