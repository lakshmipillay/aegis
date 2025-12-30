
import time
import random
import functools
from google.api_core import exceptions

def retry_with_backoff(max_retries=5, initial_delay=1.0, backoff_factor=2.0, jitter=0.5):
    """
    Retry decorator for functions that may raise 429 ResourceExhausted errors.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions.ResourceExhausted as e:
                    last_exception = e
                    if attempt == max_retries:
                        print(f"[Retry] Max retries ({max_retries}) reached. Raising error.")
                        raise
                    
                    # Calculate sleep time with jitter to avoid thundering herd
                    sleep_time = delay + random.uniform(0, jitter)
                    print(f"[Retry] 429 Resource exhausted. Retrying in {sleep_time:.2f}s (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(sleep_time)
                    delay *= backoff_factor
                except Exception as e:
                    # Reraise other exceptions immediately
                    raise e
            
            if last_exception:
                raise last_exception
        return wrapper
    return decorator
