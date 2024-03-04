from typing import TypedDict

from app.types.message import Message

type Chats = dict[int, list[Message]]


class SessionState(TypedDict):
    """
    Summary
    -------
    the StreamLit session state

    Attributes
    ----------
    chats (Chats) : the chats
    active_chat_tab (int) : the active chat tab
    """
    chats: Chats
    current_chat: int
