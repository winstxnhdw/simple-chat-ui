from streamlit import (
    button,
    rerun,
    session_state,
    sidebar,
    title,
)

from app.api import ChatAPI
from app.types import Chats


def render_delete_all_button(api: ChatAPI, chats: Chats):
    """
    Summary
    -------
    render the delete all chats button

    Parameters
    ----------
    api (ChatAPI): the chat API
    chats (Chats): the chats
    """
    if not button('Delete all', key='delete_all_chats', type='primary', use_container_width=True):
        return

    api.delete_all_chats()
    chats.clear()
    chats[1] = []
    rerun()


def render_add_chat_button(number_of_chats: int):
    """
    Summary
    -------
    render the add chat button

    Parameters
    ----------
    number_of_chats (int): the number of chat tabs
    """
    if not button('＋', key='add_chat', use_container_width=True):
        return

    chats[number_of_chats + 1] = []
    session_state['current_chat'] = number_of_chats
    rerun()


def render_chat_tab(chat: int):
    """
    Summary
    -------
    render the chat buttons

    Parameters
    ----------
    chat (int): the chats
    """
    if not button(str(chat), key=f'chat_tab_{chat}', use_container_width=True):
        return

    session_state['current_chat'] = chat
    rerun()


def render_tabs(api: ChatAPI):
    """
    Summary
    -------
    render the chat tabs

    Parameters
    ----------
    api (ChatAPI): the chat API
    """
    chats: Chats = session_state['chats']

    for chat in chats:
        render_chat_tab(chat)

    render_add_chat_button(len(chats))
    render_delete_all_button(api, chats)


def render_sidebar(api: ChatAPI):
    """
    Summary
    -------
    render the chat tabs

    Parameters
    ----------
    api (ChatAPI): the chat API
    """
    with sidebar:
        title('Chats')
        render_tabs(api)
