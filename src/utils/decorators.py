"""Utility decorators for the application."""
import threading
from functools import wraps
from typing import Any, Callable
from ..config.constants import MAX_RETRIES, RETRY_DELAY
from ..utils.logging import print_status

def timeout_decorator(seconds: int = 10):
    """Decorator to add timeout to functions."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = []
            def target():
                try:
                    result.append(func(*args, **kwargs))
                except Exception as e:
                    result.append(e)
            thread = threading.Thread(target=target)
            thread.start()
            thread.join(seconds)
            if thread.is_alive():
                raise TimeoutError(
                    f"Function {func.__name__} timed out after {seconds} seconds"
                )
            if result and isinstance(result[0], Exception):
                raise result[0]
            return result[0] if result else None
        return wrapper
    return decorator

def retry_on_error(func: Callable) -> Callable:
    """Decorator for retrying functions with proper error handling."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print_status(
                        f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {str(e)}",
                        "warning",
                    )
                    time.sleep(RETRY_DELAY)
                else:
                    print_error(e, f"Failed after {MAX_RETRIES} attempts")
                    return None
    return wrapper