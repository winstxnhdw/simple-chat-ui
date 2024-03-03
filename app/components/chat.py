from streamlit import (
    button,
    chat_input,
    chat_message,
    file_uploader,
    markdown,
    rerun,
    session_state,
    title,
)

from app.api import ChatAPI
from app.types import Chats, Message, Role


def render_prompt(api: ChatAPI, messages: list[Message], current_chat: int, image_text: str):
    """
    Summary
    -------
    render the chat prompt

    Parameters
    ----------
    api (ChatAPI): the chat API
    messages (Message): the messages
    current_chat (int): the current chat
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
    api (ChatAPI): the chat API

    Returns
    -------
    image_text (str): the image text
    """
    return (
        api.image_to_text(document)
        if (document := file_uploader('Upload an image', type=['png', 'jpg', 'jpeg']))
        else ''
    )


def render_clear_chat_button(api: ChatAPI, chats: Chats, current_chat: int):
    """
    Summary
    -------
    render the clear chat button

    Parameters
    ----------
    api (ChatAPI): the chat API
    chats (Chats): the chats
    """
    if not button('Clear chat', key=f'clear_{current_chat}'):
        return

    api.clear_chat(current_chat)
    chats[current_chat].clear()
    rerun()


def render_message(message_content: str, role: Role):
    """
    Summary
    -------
    render the chat message

    Parameters
    ----------
    message (Message): the message
    """
    with chat_message(role):
        if role == 'user':
            markdown(message_content)

        else:
            markdown(message_content)


def render_chat(api: ChatAPI):
    """
    Summary
    -------
    render the chat

    Parameters
    ----------
    api (ChatAPI): the chat API
    """
    chats: Chats = session_state['chats']
    current_chat: int = session_state['current_chat']

    if not (messages := chats[current_chat]):
        api.clear_chat(current_chat)

    title('Examplify')

    for message in messages:
        render_message(message['content'], message['role'])

    image_text = handle_document_upload(api)
    render_prompt(api, chats[current_chat], current_chat, image_text)
    render_clear_chat_button(api, chats, current_chat)
