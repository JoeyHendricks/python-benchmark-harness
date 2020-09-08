from QuickPotato.inspect.intrusive import performance_critical
import math


@performance_critical
def slow_method():
    """
    A tagged stub method that is used within the tests as a dummy slow method.
    within this method we are trying to count what the length of this number is.
    We are doing this in the most slowest way possible so we can simulate a slow method.

    Parameters
    ----------
    num An integer

    Returns
    -------
    The length of the number
    """
    num = 6 ** 6 ** 6
    return len(str(num))


@performance_critical
def fast_method():
    """
    A tagged stub method that is used within the tests as a dummy slow method.
    within this method we are trying to count what the length of this number is.
    We are doing this in the most fastest way possible so we can simulate a fast method.

    Parameters
    ----------
    num An integer

    Returns
    -------
    The length of the number
    """
    num = 6 ** 6 ** 6
    return int(math.log10(num))
