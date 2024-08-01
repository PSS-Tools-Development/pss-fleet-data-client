from typing import Optional, Union

from httpx import URL


def positive_float_or_int(
    parameter_value: Optional[Union[float, int]],
    parameter_name: str,
    default: Optional[Union[float, int]] = None,
) -> Optional[Union[float, int]]:
    """Ensures that a given parameter is a positive `float` or `int` value.

    Args:
        parameter_value (Union[float, int], optional): The parameter value to be checked.
        parameter_name (str): The name of the parameter to be checked (for a descriptive error message).
        default (Union[float, int], optional): The default value to be returned, if `parameter_value` is `None`. Defaults to `None`.

    Raises:
        ValueError: Raised, if the parameter value is negative.
        TypeError: Raised, if the parameter value is not of type `float` nor `int`.

    Returns:
        Optional[Union[float, int]]: The parameter value, if it's of type `float` or `int`. The `default` if it's `None`.
    """
    if parameter_value is None:
        return default

    if isinstance(parameter_value, (float, int)) and not isinstance(parameter_value, bool):
        if parameter_value >= 0:
            return parameter_value

        raise ValueError(f"The parameter '{parameter_name}' must not be negative.")

    raise TypeError(f"The parameter '{parameter_name}' must be of type 'float' or 'int'.")


def str_(parameter_value: Optional[str], parameter_name: str, default: Optional[str] = None) -> Optional[str]:
    """Ensures that a given parameter is of type `str`.

    Args:
        parameter_value (str, optional): The parameter value to be checked.
        parameter_name (str): The name of the parameter to be checked (for a descriptive error message).
        default (str, optional): The default value to be returned, if `parameter_value` is `None`. Defaults to `None`.

    Raises:
        TypeError: Raised, if the parameter value is not of type `str`.

    Returns:
        Optional[str]: The parameter value, if it's of type `str`. The `default` if it's `None`.
    """
    if parameter_value is None:
        return default

    if isinstance(parameter_value, str):
        return parameter_value

    raise TypeError(f"The parameter '{parameter_name}' must be of type 'str'.")


def str_or_url(
    parameter_value: Optional[Union[str, URL]],
    parameter_name: str,
    default: Optional[Union[str, URL]] = None,
) -> Optional[Union[str, URL]]:
    """Ensures that a given parameter is of type `str` or `httpx.URL`.

    Args:
        parameter_value (Union[str, httpx.URL]], optional): The parameter value to be checked.
        parameter_name (str): The name of the parameter to be checked (for a descriptive error message).
        default (Union[str, httpx.URL]], optional): The default value to be returned, if `parameter_value` is `None`. Defaults to `None`.

    Raises:
        TypeError: Raised, if the parameter value is not of type `str` nor `httpx.URL`.

    Returns:
        Optional[Union[str, httpx.URL]]]: The parameter value, if it's of type `str` or `httpx.URL`. The `default` if it's `None`.
    """
    if parameter_value is None:
        return default

    if isinstance(parameter_value, (str, URL)):
        return parameter_value

    raise TypeError(f"The parameter '{parameter_name}' must be of type 'str' or 'httpx.URL'.")
