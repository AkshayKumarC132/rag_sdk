# rag_sdk/exceptions.py

class RAGSDKException(Exception):
    """Base exception for RAG SDK"""

class AuthenticationError(RAGSDKException):
    """Raised when authentication fails"""

class APIRequestError(RAGSDKException):
    """Raised when an API request fails"""
