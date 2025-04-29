# RAG SDK

Python SDK for interacting with the RAG Django backend via REST APIs.

## Usage

```python
from rag_sdk.client import RAGClient

client = RAGClient(base_url="http://your-rag-api.com")
client.login("username", "password")
client.upload_document("file.pdf")
