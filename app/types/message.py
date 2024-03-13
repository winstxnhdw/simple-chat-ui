from typing import Literal, TypedDict

type Role = Literal['user', 'assistant']


class Message(TypedDict):
    """
    Summary
    -------
    a message in a chat

    Attributes
    ----------
    role (Role) : the role of the message (user or assistant)
    content (str) : the content of the message
    """
    role: Role
    content: str
