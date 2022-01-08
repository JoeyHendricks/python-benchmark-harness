import sys
import os


def block_print_to_console() -> None:
    """
    Used to disable the software to print to console.
    (Only used for testing purposes)
    """
    sys.stdout = open(os.devnull, 'w')


def enable_print_to_console() -> None:
    """
    Used to enable the software to print to console.
    (Only used for testing purposes)
    """
    sys.stdout = sys.__stdout__
