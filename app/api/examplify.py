from typing import Iterator

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

    __slots__ = ('client', 'base_url')

    def __init__(self, base_url: str):
        self.client = Client(http2=True, verify=False)
        self.base_url = base_url

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.client.close()

    def get_chat_history(self, chat_id: int) -> list[Message]:
        request = self.client.get(f'{self.base_url}/v1/chats/{chat_id}/messages')
        return request.json()['messages']

    def query(self, chat_id: int, query: str, search_size: int, store_query: bool) -> Iterator[str]:
        endpoint = f'{self.base_url}/v1/chats/{chat_id}/query'
        body = {'query': query}
        params = {'store_query': store_query, 'search_size': search_size}

        with connect_sse(self.client, 'POST', endpoint, json=body, params=params, timeout=None) as events:
            for event in events.iter_sse():
                yield event.data

    def image_to_text(self, file: UploadedFile) -> str:
        endpoint = f'{self.base_url}/v1/files/text'
        files = [('data', (file.name, file.getvalue(), file.type))]

        with connect_sse(self.client, 'POST', endpoint, files=files, timeout=None) as events:
            return ''.join(event.data for event in events.iter_sse())

    def clear_chat(self, chat_id: int):
        self.client.delete(f'{self.base_url}/v1/chats/{chat_id}/messages', params={'recreate': True})

    def delete_all_chats(self):
        self.client.delete(f'{self.base_url}/debug/redis')
