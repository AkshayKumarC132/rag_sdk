# rag_sdk/client.py

import requests
import os
from .exceptions import AuthenticationError, APIRequestError
from .utils import retry_on_failure

class RAGClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.timeout = timeout

    @retry_on_failure()
    def login(self, username: str, password: str) -> dict:
        url = f"{self.base_url}/login/"
        response = self._post(url, json={"username": username, "password": password})
        self.token = response["token"]
        return response

    @retry_on_failure()
    def logout(self) -> dict:
        self._ensure_authenticated()
        url = f"{self.base_url}/logout/{self.token}/"
        response = self._post(url)
        self.token = None
        return response

    @retry_on_failure()
    def upload_document(self, file_path: str) -> dict:
        print("[!] Uploading document...")
        print(file_path)
        self._ensure_authenticated()
        url = f"{self.base_url}/ingest/{self.token}/"
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            return self._post(url, files=files)

    @retry_on_failure()
    def list_documents(self) -> dict:
        self._ensure_authenticated()
        url = f"{self.base_url}/list-documents/{self.token}/"
        return self._get(url)

    @retry_on_failure()
    def ask_question(self, question: str, vector_id: str = None) -> dict:
        self._ensure_authenticated()
        url = f"{self.base_url}/ask/{self.token}/"
        payload = {"question": question}
        if vector_id:
            payload["vector_id"] = vector_id
        return self._post(url, json=payload)

    @retry_on_failure()
    def get_chat_history(self, vector_id: str) -> dict:
        self._ensure_authenticated()
        url = f"{self.base_url}/chat-history/{self.token}/{vector_id}/"
        return self._get(url)

    @retry_on_failure()
    def save_chat_history(self, vector_id: str, history: list) -> dict:
        self._ensure_authenticated()
        url = f"{self.base_url}/chat-history/{self.token}/{vector_id}/"
        return self._post(url, json={"history": history})

    @retry_on_failure()
    def clear_chat_history(self, vector_id: str) -> dict:
        self._ensure_authenticated()
        url = f"{self.base_url}/chat-history/{self.token}/{vector_id}/"
        return self._delete(url)

    @retry_on_failure()
    def retrieve_document(self, vector_id: str) -> dict:
        self._ensure_authenticated()
        url = f"{self.base_url}/retrieve/document/{self.token}/{vector_id}"
        return self._get(url)

    @retry_on_failure()
    def delete_document(self, vector_id: str) -> dict:
        self._ensure_authenticated()
        url = f"{self.base_url}/delete/{self.token}/{vector_id}"
        return self._delete(url)

    @retry_on_failure()
    def ask_multifile(self, question: str, vector_ids: list) -> dict:
        self._ensure_authenticated()
        url = f"{self.base_url}/multifile-ask/{self.token}/"
        payload = {"question": question, "vector_ids": vector_ids}
        return self._post(url, json=payload)

    @retry_on_failure()
    def global_ask(self, question: str) -> dict:
        self._ensure_authenticated()
        url = f"{self.base_url}/global-ask/{self.token}/"
        payload = {"question": question}
        return self._post(url, json=payload)

    @retry_on_failure()
    def get_document_alerts(self, vector_id: str) -> dict:
        url = f"{self.base_url}/document-alerts/{vector_id}/"
        return self._get(url)

    # Internal helpers

    def _ensure_authenticated(self):
        if not self.token:
            raise AuthenticationError("You must login first.")

    def _get(self, url, **kwargs):
        return self._request("GET", url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request("POST", url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request("DELETE", url, **kwargs)

    def _request(self, method, url, **kwargs):
        try:
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise APIRequestError(f"API error {response.status_code}: {response.text}") from e
        except requests.exceptions.RequestException as e:
            raise APIRequestError("Request failed") from e
