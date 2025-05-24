import time
from functools import wraps

def timed_crud(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"[CRUD Timer] {func.__name__} took {duration:.4f}s")
        return result
    return wrapper
