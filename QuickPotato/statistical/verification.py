

def check_max_boundary_of_measurement(value, boundary):
    """
    :return:
    """
    if boundary is None:
        return None

    elif float(value) < float(boundary):
        return True

    else:
        return False


def check_min_boundary_of_measurement(value, boundary):
    """
    :return:
    """
    if boundary is None:
        return None

    elif float(value) > float(boundary):
        return True

    else:
        return False
