from QuickPotato.harness.reporting import BoundariesTestReport, RegressionTestReport
from QuickPotato.utilities.exceptions import NeedsKeyWordArguments
from functools import wraps


def save_evidence_test_report(fnc):
    """

    Parameters
    ----------
    fnc

    Returns
    -------

    """

    @wraps(fnc)
    def encapsulated_method(*args, **kwargs):
        """

        Parameters
        ----------
        args
        kwargs

        Returns
        -------

        """
        if len(args) > 1:
            raise NeedsKeyWordArguments()

        if str(fnc.__name__) == "run_t_test":

            report = RegressionTestReport()
            report.test_id = args[0].test_id
            report.test_case_name = args[0].test_case_name
            report.t_test_status = fnc(*args, **kwargs)
            report.t_test_value = float(args[0].t_value)
            report.t_test_critical_value = float(args[0].critical_t_value)
            report.save()

            return report.t_test_status

        elif str(fnc.__name__) == "run_f_test":

            report = RegressionTestReport()
            report.test_id = args[0].test_id
            report.test_case_name = args[0].test_case_name
            report.f_test_status = fnc(*args, **kwargs)
            report.f_test_value = float(args[0].f_value)
            report.f_test_critical_value = float(args[0].critical_f_value)
            report.save()

            return report.f_test_status

        else:

            report = BoundariesTestReport()
            report.test_id = kwargs["test_id"]
            report.test_case_name = kwargs["test_case_name"]
            report.verification_name = kwargs["validation_name"]
            report.metric = kwargs["metric"]
            report.threshold = kwargs["threshold"]

            # Scrub unused meta data
            del kwargs["test_id"]
            del kwargs["test_case_name"]
            del kwargs["validation_name"]

            report.verification_status = fnc(*args, **kwargs)
            report.save()

            return report.verification_status

    return encapsulated_method


def save_to_test_report(fnc):
    """

    Parameters
    ----------
    fnc

    Returns
    -------

    """

    @wraps(fnc)
    def encapsulated_method(*args, **kwargs):
        """

        Parameters
        ----------
        args
        kwargs

        Returns
        -------

        """
        if str(fnc.__name__) == "verify_that_there_is_no_change_between_the_baseline_and_benchmark":

            instance = args[0]
            report = RegressionTestReport()
            report.test_id = instance.current_test_id
            report.test_case_name = instance.test_case_name
            report.status = fnc(*args, **kwargs)
            report.save()
            return report.status

        elif str(fnc.__name__) == "verify_if_benchmark_does_not_breach_defined_boundaries":

            instance = args[0]
            report = BoundariesTestReport()
            report.test_id = instance.current_test_id
            report.test_case_name = instance.test_case_name
            report.status = fnc(*args, **kwargs)
            report.save()
            return report.status

        else:
            raise NotImplementedError

    return encapsulated_method
