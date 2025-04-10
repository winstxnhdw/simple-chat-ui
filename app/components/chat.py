from __future__ import annotations

from httpx import ConnectError
from streamlit import (
    button,
    chat_input,
    chat_message,
    file_uploader,
    markdown,
    rerun,
    slider,
    tabs,
    title,
    toggle,
    write_stream,
)

from app.api import ChatAPI
from app.helpers import try_connect
from app.types import Chats, Message, Role, SessionState


def render_clear_chat_button(api: ChatAPI, chats: Chats, current_chat: int) -> None:
    """
    Summary
    -------
    render the clear chat button

    Parameters
    ----------
    api (ChatAPI)
        the API object

    chats (Chats)
        the sequence of all chats

    current_chat (int)
        the current chat identifier
    """
    if not button("Clear chat", key=f"clear_chat_{current_chat}"):
        return

    api.clear_chat(current_chat)
    chats[current_chat].clear()
    rerun()


def render_prompt(
    api: ChatAPI,
    messages: list[Message],
    current_chat: int,
    image_text: str,
    search_size: int,
    *,
    store_query: bool,
) -> None:
    """
    Summary
    -------
    render the chat prompt

    Parameters
    ----------
    api (ChatAPI)
        the API object

    messages (list[Message])
        the sequence of messages

    current_chat (int)
        the current chat identifier

    image_text (str)
        the text in the image

    search_size (int)
        the search size

    store_query (bool)
        whether to store the query
    """
    if not (prompt := chat_input("What is up?")):
        return

    prompt = f"{prompt}\n\n{image_text}"
    messages.append({"role": "user", "content": prompt})

    with chat_message("user"):
        markdown(prompt)

    with chat_message("assistant"):
        response = api.query(current_chat, prompt, search_size, store_query=store_query)
        content: str = write_stream(response)  # pyright: ignore [reportAssignmentType]
        messages.append({"role": "assistant", "content": content})


def handle_document_upload(api: ChatAPI) -> str:
    """
    Summary
    -------
    handle the document upload

    Parameters
    ----------
    api (ChatAPI)
        the chat API

    Returns
    -------
    image_text (str)
        the image text

    """
    return (
        api.image_to_text(document)
        if (document := file_uploader("Upload an image", type=["png", "jpg", "jpeg"]))
        else ""
    )


def render_message(message_content: str, role: Role) -> None:
    """
    Summary
    -------
    render the chat message

    Parameters
    ----------
    message (Message)
        the message

    role (Role)
        the message owner's role
    """
    with chat_message(role):
        if role == "user":
            markdown(message_content)

        else:
            markdown(message_content)


@try_connect(connect_exception=ConnectError, retry_delay=1.0)
def sync_chat_state(api: ChatAPI, current_chat: int) -> list[Message] | None:
    """
    Summary
    -------
    poll the API connection and sync the chat state with the API

    Parameters
    ----------
    api (ChatAPI)
        the API object

    current_chat (int)
        the current chat identifier

    chat_messages (list[Message])
        the sequence of messages
    """
    if chat_messages := api.get_chat_history(current_chat):
        return chat_messages

    api.clear_chat(current_chat)
    return None


def render_chat_tab(api: ChatAPI, chats: Chats, current_chat: int, search_size: int, *, store_query: bool) -> None:
    """
    Summary
    -------
    render the chat tab

    Parameters
    ----------
    api (ChatAPI)
        the API object

    chats (Chats)
        the sequence of all chats

    current_chat (int)
        the current chat identifier

    search_size (int)
        the search size

    store_query (bool)
        whether to store the query
    """
    title("Examplify")

    for message in sync_chat_state(api, current_chat) or []:
        render_message(message["content"], message["role"])

    image_text = handle_document_upload(api)
    render_prompt(api, chats[current_chat], current_chat, image_text, search_size, store_query=store_query)
    render_clear_chat_button(api, chats, current_chat)


def render_settings_tab(state: SessionState) -> None:
    """
    Summary
    -------
    render the settings tab

    Parameters
    ----------
    state (SessionState)
        the Streamlit session state
    """
    state["store_query"] = toggle("Store query", value=True)
    state["search_size"] = slider("Search size", 0, 10)


def render_chat(api: ChatAPI, state: SessionState) -> None:
    """
    Summary
    -------
    render the chat

    Parameters
    ----------
    api (ChatAPI)
        the API object

    state (SessionState)
        the Streamlit session state
    """
    chat_tab, settings_tab = tabs(["Chat", "Settings"])

    with settings_tab:
        render_settings_tab(state)

    with chat_tab:
        render_chat_tab(
            api,
            state["chats"],
            state["current_chat"],
            state["search_size"],
            store_query=state["store_query"],
        )
