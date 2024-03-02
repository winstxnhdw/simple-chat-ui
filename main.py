# pylint: disable=missing-class-docstring, missing-function-docstring, invalid-name

from typing import Literal, TypedDict

from httpx import get, post
from streamlit import (
    button,
    chat_input,
    chat_message,
    file_uploader,
    markdown,
    rerun,
    session_state,  # type: ignore
    sidebar,
    title,
)
from streamlit.runtime.uploaded_file_manager import UploadedFile

type Role = Literal['user', 'assistant']

class Message(TypedDict):
    content: str
    role: Role


class SessionState(TypedDict):
    chats: dict[int, list[Message]]
    active_chat_tab: int


def generate(query: str, chat_id: int) -> list[Message]:
    return post(
        f'http://localhost:5000/api/v1/{chat_id}/query',
        json={ 'query': query },
        timeout=None
    ).json()['messages']


def get_image_from_text(file: UploadedFile) -> str:
    return post(
        'http://localhost:5000/api/debug/image_to_text',
        files={ 'request': (file.name, file.getvalue(), file.type) },
        timeout=None
    ).text


def render_text(text_to_render: str, role: Role):
    if role == 'user':
        markdown(text_to_render)

    else:
        markdown(text_to_render)


def clear_chat(chat_id: int):
    get(f'http://localhost:5000/api/v1/{chat_id}/clear_chat')


def delete_all():
    get('http://localhost:5000/api/debug/delete_all')


session_state: SessionState

if 'chats' not in session_state:
    session_state['chats'] = { 1: [] }

if 'active_chat_tab' not in session_state:
    session_state['active_chat_tab'] = 1

chats: dict[int, list[Message]] = session_state['chats']
active_chat_tab = session_state['active_chat_tab']
messages = chats[active_chat_tab]

if not messages:
    clear_chat(active_chat_tab)

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
        delete_all()
        chats.clear()
        chats[1] = []
        rerun()

if button('Clear chat', key=f'clear_{active_chat_tab}'):
    clear_chat(active_chat_tab)
    messages.clear()
    rerun()

for message in messages:
    with chat_message(message['role']):
        render_text(message['content'], message['role'])

image_text = ''

if document := file_uploader('Upload an image', type=['png', 'jpg', 'jpeg']):
    image_text = get_image_from_text(document)

if prompt := chat_input('What is up?'):
    prompt = f'{prompt}\n\n{image_text}'
    messages.append({ 'content': prompt, 'role': 'user' })

    with chat_message('user'):
        markdown(prompt)

    with chat_message('assistant'):
        response = generate(prompt, active_chat_tab)[-1]
        markdown(response['content'])
        messages.append(response)
