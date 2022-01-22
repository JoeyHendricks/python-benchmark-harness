from .._utilities.exceptions import NoAnnotationFoundOnMethod
from functools import wraps


def verify_method_annotations(method):

    @wraps(method)
    def execution(*args: list, **kwargs: dict):
        """
        Will execute the method if either the args or kwargs match
        the expected type hints, this method should only be applied
        to methods that use type hints.
        :param args: The postional arguments
        :param kwargs: The key word arguments
        :return: The output of the function or method.
        """
        if len(method.__annotations__) == 0:
            raise NoAnnotationFoundOnMethod()

        # verify if given key word arguments match annotations.
        elif len(kwargs) > 0:
            for given_variable in kwargs:
                if type(kwargs[given_variable]) == method.__annotations__[given_variable]:
                    continue

                else:
                    raise TypeError(
                        f"Error: {kwargs[given_variable]} is of type: {type(kwargs[given_variable])},"
                        f" should be of type: {method.__annotations__[given_variable]}"
                    )

        else:
            # Will create a list out of args and delete an reference of self out of methods.
            positional_arguments = list(args)
            if isinstance(positional_arguments[0], object):
                del positional_arguments[0]

            # verify if given positional arguments match annotations
            for given_variable, expected_variable in zip(positional_arguments, method.__annotations__):
                print(f"{given_variable}--{expected_variable}")
                if type(given_variable) == method.__annotations__[expected_variable]:
                    continue

                else:
                    raise TypeError(
                        f"Error: {given_variable} is of type: {type(given_variable)},"
                        f" should be of type: {method.__annotations__[expected_variable]}"
                    )

        return method(*args, **kwargs)

    return execution


def takes_arguments(function):
    """
    A decorator for a decorator that should take arguments.
    With the purpose to make other decorator that use
    arguments less complicated.

    more info: https://stackoverflow.com/questions/5929107/decorators-with-parameters

    :param function: The decorator that should take arguments
    :return:
    """

    def decorator(*args, **kwargs):
        def wrapper(f):
            return function(f, *args, **kwargs)

        return wrapper

    return decorator
