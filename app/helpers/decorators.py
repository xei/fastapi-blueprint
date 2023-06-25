import functools
import time



def cache_result(func):
    """
    This decorator caches the result of a coroutine
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        cache_key = str(args) + str(kwargs)
        if cache_key not in wrapper.cache:
            result = await func(*args, **kwargs)
            wrapper.cache[cache_key] = result
        return wrapper.cache[cache_key]
    wrapper.cache = {}
    return wrapper


def calculate_execution_time(func):
    """
    This decorator calculates the execution time of a coroutine and
    put it in a dictionary besides the result itself.
    """
    async def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = await func(*args, **kwargs)
        end_time = time.monotonic()
        return {
            "function_name": func.__name__,
            "result": result,
            "execution_time_ms": (end_time - start_time) * 1000
        }
    return wrapper