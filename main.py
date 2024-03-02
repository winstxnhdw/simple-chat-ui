from typing import Literal, TypedDict

from httpx import get, post
from streamlit import (
    chat_input,
    chat_message,
    markdown,
    session_state,  # type: ignore
    title,
    write,
)


class Query(TypedDict):
    query: str


class Message(TypedDict):
    content: str
    role: Literal['user', 'assistant']


class SessionState:
    messages: list[Message]


def generate(query: Query) -> list[Message]:
    return post("http://localhost:5000/api/v1/1/query", json=query, timeout=None).json()['messages']


get("http://localhost:5000/api/v1/1/clear_chat")

title("Examplify")

session_state: SessionState

if "messages" not in session_state: # type: ignore
    session_state.messages = []

for message in session_state.messages:
    with chat_message(message["role"]):
        markdown(message["content"])

if prompt := chat_input("What is up?"):
    with chat_message("user"):
        markdown(prompt)

    with chat_message("assistant"):
        response = generate({ "query": prompt })[-1]
        write(response["content"])

    session_state.messages.append(response)
