from time import sleep
from typing import Any, Callable, TypeVar

from httpx import ConnectError

T = TypeVar('T')

Function = Callable[..., T]


def wrapper(function: Function[T], retry_delay: float, *args: Any, **kwargs: Any) -> T:
    """
    Summary
    -------
    wrap the function with a retry loop

    Parameters
    ----------
    function (Wrapper[T]) : the function to wrap
    retry_delay (float) : the delay between retries

    Returns
    -------
    result (T) : the result of the function
    """
    while True:
        try:
            return function(*args, **kwargs)

        except ConnectError:
            sleep(retry_delay)


def try_connect_decorator(function: Function[T], retry_delay: float) -> Function[T]:
    """
    Summary
    -------
    create a decorator that wraps the function with a retry loop

    Parameters
    ----------
    function (Wrapper[T]) : the function to wrap
    retry_delay (float) : the delay between retries

    Returns
    -------
    wrapper (Wrapper[T]) : the wrapped function
    """
    return lambda *args, **kwargs: wrapper(function, retry_delay, *args, **kwargs)


def try_connect(*, retry_delay: float = 1.0) -> Callable[[Function[T]], Function[T]]:
    """
    Summary
    -------
    create a decorator that wraps the function with a retry loop

    Parameters
    ----------
    retry_delay (float?) : the delay between retries

    Returns
    -------
    decorator (Callable[[Wrapper[T]], Wrapper[T]]) : the decorator
    """
    return lambda function: try_connect_decorator(function, retry_delay)
