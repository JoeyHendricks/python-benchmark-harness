from QuickPotato.harness.results import BoundariesTestEvidence
from functools import wraps
from datetime import datetime


def save_boundary_evidence(fnc):
    """

    Parameters
    ----------
    fnc

    Returns
    -------

    """

    @wraps(fnc)
    def encapsulated_function(*args, **kwargs):
        """

        Parameters
        ----------
        args
        kwargs

        Returns
        -------

        """
        evidence = BoundariesTestEvidence()
        evidence.test_id = kwargs["test_id"]
        evidence.test_case_name = kwargs["test_case_name"]
        evidence.epoch_timestamp = datetime.now().timestamp()
        evidence.human_timestamp = datetime.now()
        evidence.verification_name = kwargs["validation_name"]
        evidence.value = float(kwargs["value"])
        evidence.boundary = float(kwargs["boundary"])

        # Scrub unused meta data
        del kwargs["test_id"]
        del kwargs["test_case_name"]
        del kwargs["validation_name"]

        evidence.status = fnc(*args, **kwargs)
        evidence.save()

        return evidence.status

    return encapsulated_function
