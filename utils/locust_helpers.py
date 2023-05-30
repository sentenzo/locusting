import time

from locust import events


def self_firing(*, request_type, name):
    def decorator(func):
        def wrapper(*args, **kwds):
            start_time = time.time()
            exception = None
            result = None
            try:
                result = func(*args, **kwds)
            except Exception as ex:
                exception = ex
            events.request.fire(
                request_type=request_type,
                name=name,
                response_length=0,
                start_time=start_time,
                response_time=time.time() - start_time,
                exception=exception,
            )
            return result

        return wrapper

    return decorator
