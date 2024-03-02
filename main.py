# pylint: disable=missing-class-docstring, missing-function-docstring

from typing import Literal, TypedDict

from httpx import get, post
from streamlit import (
    button,
    chat_input,
    chat_message,
    markdown,
    rerun,
    session_state,  # type: ignore
    sidebar,
    title,
    write,
)


class Query(TypedDict):
    query: str


class Message(TypedDict):
    content: str
    role: Literal['user', 'assistant']


class SessionState(TypedDict):
    chats: dict[int, list[Message]]
    active_chat_tab: int


def generate(query: Query, chat_id: int) -> list[Message]:
    return post(f'http://localhost:5000/api/v1/{chat_id}/query', json=query, timeout=None).json()['messages']


session_state: SessionState

if 'chats' not in session_state:
    session_state['chats'] = { 1: [] }

if 'active_chat_tab' not in session_state:
    session_state['active_chat_tab'] = 1

chats: dict[int, list[Message]] = session_state['chats']
active_chat_tab = session_state['active_chat_tab']
messages = chats[active_chat_tab]

title('Examplify')

with sidebar:
    title('Chats')

    for chat_tab in chats:
        if button(str(chat_tab), key=f'chat_tab_{chat_tab}', use_container_width=True):
            session_state['active_chat_tab'] = chat_tab
            rerun()

    if button('＋', key=f'add_{active_chat_tab}', use_container_width=True):
        chats[len(chats) + 1] = []
        active_chat_tab = len(chats)
        rerun()

    if button('Delete all', key=f'delete_all_{active_chat_tab}', type='primary', use_container_width=True):
        get('http://localhost:5000/api/debug/delete_all')
        chats.clear()
        chats[1] = []
        rerun()

if button('Clear chat', key=f'clear_{active_chat_tab}'):
    get(f'http://localhost:5000/api/v1/{active_chat_tab}/clear_chat')
    messages.clear()
    rerun()

for message in messages:
    with chat_message(message['role']):
        markdown(message['content'])

if prompt := chat_input('What is up?'):
    messages.append({ 'content': prompt, 'role': 'user' })

    with chat_message('user'):
        markdown(prompt)

    with chat_message('assistant'):
        response = generate({ 'query': prompt }, active_chat_tab)[-1]
        write(response['content'])

    messages.append(response)
