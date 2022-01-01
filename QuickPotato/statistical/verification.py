

def check_max_boundary_of_measurement(value: float, boundary: float) -> bool or None:
    """
    :return:
    """
    if boundary is None:
        return None

    elif value < boundary:
        return True

    else:
        return False


def check_min_boundary_of_measurement(value: float, boundary: float) -> bool or None:
    """
    :return:
    """
    if boundary is None:
        return None

    elif value > boundary:
        return True

    else:
        return False
