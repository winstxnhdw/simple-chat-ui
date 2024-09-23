from typing import Iterator, Protocol

from streamlit.runtime.uploaded_file_manager import UploadedFile

from app.types import Message


class ChatAPI(Protocol):
    """
    Summary
    -------
    a generic chat API protocol

    Methods
    -------
    query(chat_id: int, query: str) -> list[Message]
        query the chat API

    image_to_text(file: UploadedFile) -> str
        convert an image to text

    clear_chat(chat_id: int)
        clear a specific chat

    delete_all_chats()
        delete all chats
    """

    def __init__(self, base_url: str): ...

    def get_chat_history(self, chat_id: int) -> list[Message]:
        """
        Summary
        -------
        get the chat history

        Parameters
        ----------
        chat_id (int) : the chat ID

        Returns
        -------
        list[Message] : the chat history
        """
        ...

    def query(self, chat_id: int, query: str, search_size: int, store_query: bool) -> Iterator[str]:
        """
        Summary
        -------
        query the chat API

        Parameters
        ----------
        chat_id (int) : the chat ID
        query (str) : the query to send
        search_size (int) : the search size
        store_query (bool) : whether to store the query

        Returns
        -------
        list[Message]: the messages returned
        """
        ...

    def image_to_text(self, file: UploadedFile) -> str:
        """
        Summary
        -------
        convert an image to text

        Parameters
        ----------
        file (UploadedFile) : the image file to convert

        Returns
        -------
        text (str) : the text in the image
        """
        ...

    def clear_chat(self, chat_id: int):
        """
        Summary
        -------
        clear a specific chat

        Parameters
        ----------
        chat_id (int) : the chat ID
        """

    def delete_all_chats(self):
        """
        Summary
        -------
        delete all chats
        """
