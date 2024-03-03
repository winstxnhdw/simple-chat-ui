from typing import Protocol

from streamlit.runtime.uploaded_file_manager import UploadedFile

from app.types import Message


class ChatAPI(Protocol):
    """
    Summary
    -------
    a generic chat API protocol
    """
    def __init__(self, base_url: str): ...


    def query(self, chat_id: int, query: str) -> list[Message]:
        """
        Summary
        -------
        query the chat API

        Parameters
        ----------
        chat_id (int): the chat ID
        query (str): the query to send

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
        file (UploadedFile): the image file to convert

        Returns
        -------
        text (str): the text in the image
        """
        ...


    def clear_chat(self, chat_id: int):
        """
        Summary
        -------
        clear a specific chat

        Parameters
        ----------
        chat_id (int): the chat ID
        """


    def delete_all_chats(self):
        """
        Summary
        -------
        delete all chats
        """
