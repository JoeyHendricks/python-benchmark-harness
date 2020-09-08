from QuickPotato.harness.reporting import BoundariesTestReport, RegressionTestReport
from QuickPotato.utilities.exceptions import NeedsKeyWordArguments
from functools import wraps


def save_evidence_to_boundaries_test_report(fnc):
    """
    Provides a global way to store non-functional requirements in a test report.
    This method is used as decorator to encapsulate every NFR validation.
    Parameters

    Please note that this decorator does not support positional arguments.

    Parameters
    ----------
    fnc: The validation method and it parameters that need to be encapsulated.

    Returns
    -------
    The output of the function either True or False.
    """

    @wraps(fnc)
    def encapsulated_method(*args, **kwargs):
        """
        Will wrap around the original method and process its data.

        Note that the wrapper will delete variables from kwargs that are not needed
        in the validation.

        Parameters
        ----------
        args (unsupported)
        kwargs (Supported) contains the keys, test_id test_case_name and metric.

        Raises
        -------
        DecoratorNeedsKeyWordArguments
            Is raised when positional arguments are used.

        Returns
        -------
        The output of the function either True or False.
        """
        if len(args) > 1:
            raise NeedsKeyWordArguments()

        # Note down test meta data
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

        # Execute validation
        function_output = fnc(*args, **kwargs)

        # Note down test output
        report.verification_status = function_output
        report.save()

        return function_output

    return encapsulated_method


def save_f_test_evidence_to_regression_test_report(fnc):
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
        instance = args[0]
        report = RegressionTestReport()
        report.test_id = instance.test_id
        report.test_case_name = instance.test_case_name
        report.f_test_status = fnc(*args, **kwargs)
        report.f_test_value = float(instance.f_value)
        report.f_test_critical_value = float(instance.critical_f_value)
        report.save()

        return report.f_test_status

    return encapsulated_method


def save_t_test_evidence_to_regression_test_report(fnc):
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
        instance = args[0]
        report = RegressionTestReport()
        report.test_id = instance.test_id
        report.test_case_name = instance.test_case_name
        report.t_test_status = fnc(*args, **kwargs)
        report.t_test_value = float(instance.t_value)
        report.t_test_critical_value = float(instance.critical_t_value)
        report.save()

        return report.t_test_status

    return encapsulated_method


def save_to_regression_test_report(fnc):
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
        if str(fnc.__name__) == "analyse_benchmark_against_baseline_for_regression":

            instance = args[0]
            report = RegressionTestReport()
            report.test_id = instance.current_test_id
            report.test_case_name = instance.test_case_name
            report.status = fnc(*args, **kwargs)
            report.save()

            return report.status

        else:
            raise NotImplementedError

    return encapsulated_method
