from streamlit import (
    button,
    chat_input,
    chat_message,
    file_uploader,
    markdown,
    rerun,
    title,
)

from app.api import ChatAPI
from app.helpers import try_connect
from app.types import Chats, Message, Role, SessionState


def render_clear_chat_button(api: ChatAPI, chats: Chats, current_chat: int):
    """
    Summary
    -------
    render the clear chat button

    Parameters
    ----------
    api (ChatAPI) : the API object
    chats (Chats) : the sequence of all chats
    current_chat (int) : the current chat identifier
    """
    if not button('Clear chat', key=f'clear_chat_{current_chat}'):
        return

    api.clear_chat(current_chat)
    chats[current_chat].clear()
    rerun()


def render_prompt(api: ChatAPI, messages: list[Message], current_chat: int, image_text: str):
    """
    Summary
    -------
    render the chat prompt

    Parameters
    ----------
    api (ChatAPI) : the API object
    messages (list[Message]) : the sequence of messages
    current_chat (int) : the current chat identifier
    image_text (str) : the text in the image
    """
    if not (prompt := chat_input('What is up?')):
        return

    prompt = f'{prompt}\n\n{image_text}'
    messages.append({ 'content': prompt, 'role': 'user' })

    with chat_message('user'):
        markdown(prompt)

    with chat_message('assistant'):
        response = api.query(current_chat, prompt)[-1]
        messages.append(response)
        markdown(response['content'])


def handle_document_upload(api: ChatAPI) -> str:
    """
    Summary
    -------
    handle the document upload

    Parameters
    ----------
    api (ChatAPI) : the chat API

    Returns
    -------
    image_text (str) : the image text
    """
    return (
        api.image_to_text(document)
        if (document := file_uploader('Upload an image', type=['png', 'jpg', 'jpeg']))
        else ''
    )


def render_message(message_content: str, role: Role):
    """
    Summary
    -------
    render the chat message

    Parameters
    ----------
    message (Message) : the message
    role (Role) : the message owner's role
    """
    with chat_message(role):
        if role == 'user':
            markdown(message_content)

        else:
            markdown(message_content)


@try_connect(retry_delay=1.0)
def sync_chat_state(api: ChatAPI, current_chat: int, chat_messages: list[Message]):
    """
    Summary
    -------
    poll the API connection and sync the chat state with the API

    Parameters
    ----------
    api (ChatAPI) : the API object
    current_chat (int) : the current chat identifier
    chat_messages (list[Message]) : the sequence of messages
    """
    if chat_messages:
        return

    api.clear_chat(current_chat)


def render_chat(api: ChatAPI, state: SessionState):
    """
    Summary
    -------
    render the chat

    Parameters
    ----------
    api (ChatAPI) : the API object
    """
    chats = state['chats']
    current_chat = state['current_chat']
    sync_chat_state(api, current_chat, messages := chats[current_chat])
    title('Examplify')

    for message in messages:
        render_message(message['content'], message['role'])

    image_text = handle_document_upload(api)
    render_prompt(api, chats[current_chat], current_chat, image_text)
    render_clear_chat_button(api, chats, current_chat)
