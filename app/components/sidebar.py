from streamlit import (
    button,
    rerun,
    sidebar,
    title,
)

from app.api import ChatAPI
from app.helpers import SESSION_STATE
from app.types import Chats


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


def render_add_chat_button(chats: Chats):
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
    SESSION_STATE['current_chat'] = number_of_chats
    rerun()


def render_chat_tab(chat: int):
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

    SESSION_STATE['current_chat'] = chat
    rerun()


def render_tabs(api: ChatAPI):
    """
    Summary
    -------
    render the chat tabs

    Parameters
    ----------
    api (ChatAPI) : the API object
    """
    chats = SESSION_STATE['chats']

    for chat in chats:
        render_chat_tab(chat)

    render_add_chat_button(chats)
    render_delete_all_button(api, chats)


def render_sidebar(api: ChatAPI):
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
        render_tabs(api)
