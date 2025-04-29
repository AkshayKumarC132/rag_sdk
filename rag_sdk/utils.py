# rag_sdk/utils.py

import time
import functools
import requests

def retry_on_failure(max_retries=3, delay=2):
    """Retry decorator for handling temporary failures"""
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries:
                        raise
                    print(f"[!] Request failed (attempt {attempt}), retrying after {delay} sec...")
                    time.sleep(delay)
        return wrapper_retry
    return decorator_retry
