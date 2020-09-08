from QuickPotato.utilities.decorators import save_evidence_to_boundaries_test_report


@save_evidence_to_boundaries_test_report
def validate_max_boundary_of_measurements(metric, threshold):
    """
    :return:
    """
    if threshold is None:
        return None

    elif float(metric) < float(threshold):
        return True

    else:
        return False


@save_evidence_to_boundaries_test_report
def validate_min_boundary_of_measurements(metric, threshold):
    """
    :return:
    """
    if threshold is None:
        return None

    elif float(metric) > float(threshold):
        return True

    else:
        return False
