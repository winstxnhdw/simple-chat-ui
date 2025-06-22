from collections.abc import Callable
from time import sleep


def wrapper[**P, R](
    function: Callable[P, R],
    connect_exception: type[Exception],
    retry_delay: float,
    *args: P.args,
    **kwargs: P.kwargs,
) -> R:
    """
    Summary
    -------
    wrap the function with a retry loop

    Parameters
    ----------
    function (Callable[P, R])
        the function to wrap

    connect_exception (Exception)
        the exception to catch

    retry_delay (float)
        the delay between retries


    Returns
    -------
    result (R)
        the result of the function
    """
    while True:
        try:
            return function(*args, **kwargs)

        except connect_exception:
            sleep(retry_delay)


def try_connect_decorator[**P, R](
    function: Callable[P, R],
    connect_exception: type[Exception],
    retry_delay: float,
) -> Callable[P, R]:
    """
    Summary
    -------
    create a decorator that wraps the function with a retry loop

    Parameters
    ----------
    function (Callable[P, R])
        the function to wrap

    connect_exception (Exception)
        the exception to catch

    retry_delay (float)
        the delay between retries


    Returns
    -------
    wrapper (Callable[P, R])
        the wrapped function
    """
    return lambda *args, **kwargs: wrapper(function, connect_exception, retry_delay, *args, **kwargs)


def try_connect[**P, R](
    *,
    connect_exception: type[Exception] = Exception,
    retry_delay: float = 1.0,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Summary
    -------
    create a decorator that wraps the function with a retry loop

    Parameters
    ----------
    connect_exception (Exception?)
        the exception to catch

    retry_delay (float?)
        the delay between retries


    Returns
    -------
    decorator (Callable[[Callable[P, R]], Callable[P, R]])
        the decorator
    """
    return lambda function: try_connect_decorator(function, connect_exception, retry_delay)
