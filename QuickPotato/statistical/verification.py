from QuickPotato.utilities.decorators import save_boundary_evidence


@save_boundary_evidence
def validate_max_boundary_of_measurements(value, boundary):
    """
    :return:
    """
    if boundary is None:
        return None

    elif float(value) < float(boundary):
        return True

    else:
        return False


@save_boundary_evidence
def validate_min_boundary_of_measurements(value, boundary):
    """
    :return:
    """
    if boundary is None:
        return None

    elif float(value) > float(boundary):
        return True

    else:
        return False
