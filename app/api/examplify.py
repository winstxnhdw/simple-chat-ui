from httpx import Client
from streamlit.runtime.uploaded_file_manager import UploadedFile

from app.api.chatapi import ChatAPI
from app.types import Message


class Examplify(ChatAPI):
    """
    Summary
    -------
    the Examplify chat API
    """
    __slots__ = ('client', 'base_url')

    def __init__(self, base_url: str):

        self.client = Client(http2=True, verify=False)
        self.base_url = base_url


    def __enter__(self):

        return self


    def __exit__(self, *_):

        self.client.close()


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
        request = self.client.post(
            f'{self.base_url}/api/v1/{chat_id}/query',
            json={ 'query': query },
            timeout=None
        )

        return request.json()['messages']


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
        request = self.client.post(
            f'{self.base_url}/api/debug/image_to_text',
            files={ 'request': (file.name, file.getvalue(), file.type) },
            timeout=None
        )

        return request.text


    def clear_chat(self, chat_id: int):
        """
        Summary
        -------
        clear a specific chat

        Parameters
        ----------
        chat_id (int): the chat ID
        """
        self.client.delete(f'{self.base_url}/api/v1/{chat_id}/clear_chat')


    def delete_all_chats(self):
        """
        Summary
        -------
        delete all chats
        """
        self.client.delete(f'{self.base_url}/api/debug/delete_all')
