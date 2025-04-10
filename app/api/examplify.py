from collections.abc import Iterator
from typing import Self

from httpx import Client
from httpx_sse import connect_sse
from streamlit.runtime.uploaded_file_manager import UploadedFile

from app.api.chatapi import ChatAPI
from app.types import Message


class Examplify(ChatAPI):
    """
    Summary
    -------
    the Examplify chat API
    """

    __slots__ = ("base_url", "client")

    def __init__(self, base_url: str) -> None:
        """
        Summary
        -------
        initialises the API

        Parameters
        ----------
        base_url (str)
            the base URL of the API
        """
        self.client = Client(http2=True, verify=False)  # noqa: S501
        self.base_url = base_url

    def __enter__(self) -> Self:
        """
        Summary
        -------
        enters the context manager
        """
        return self

    def __exit__(self, *_) -> None:
        """
        Summary
        -------
        closes the client
        """
        self.client.close()

    def get_chat_history(self, chat_id: int) -> list[Message]:
        """
        Summary
        -------
        get the chat history

        Parameters
        ----------
        chat_id (int)
            the chat ID
        """
        request = self.client.get(f"{self.base_url}/v1/chats/{chat_id}/messages")
        return request.json()["messages"]

    def query(self, chat_id: int, query: str, search_size: int, *, store_query: bool) -> Iterator[str]:
        """
        Summary
        -------
        query the chat API

        Parameters
        ----------
        chat_id (int)
            the chat ID

        query (str)
            the query to send

        search_size (int)
            the search size

        store_query (bool)
            whether to store the query

        Returns
        -------
        response (list[Message])
            the messages returned
        """
        endpoint = f"{self.base_url}/v1/chats/{chat_id}/query"
        body = {"query": query}
        params = {"store_query": store_query, "search_size": search_size}

        with connect_sse(self.client, "POST", endpoint, json=body, params=params, timeout=None) as events:
            for event in events.iter_sse():
                yield event.data

    def image_to_text(self, file: UploadedFile) -> str:
        """
        Summary
        -------
        convert an image to text

        Parameters
        ----------
        file (UploadedFile)
            the image file to convert


        Returns
        -------
        text (str)
            the text in the image
        """
        endpoint = f"{self.base_url}/v1/files/text"
        files = [("data", (file.name, file.getvalue(), file.type))]

        with connect_sse(self.client, "POST", endpoint, files=files, timeout=None) as events:
            return "".join(event.data for event in events.iter_sse())

    def clear_chat(self, chat_id: int) -> None:
        """
        Summary
        -------
        clear a specific chat

        Parameters
        ----------
        chat_id (int)
            the chat ID
        """
        self.client.delete(f"{self.base_url}/v1/chats/{chat_id}/messages", params={"recreate": True})

    def delete_all_chats(self) -> None:
        """
        Summary
        -------
        delete all chats
        """
        self.client.delete(f"{self.base_url}/debug/redis")
