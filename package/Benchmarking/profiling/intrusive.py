from ..profiling.interpreters import ProfilerStatisticsInterpreter
from .._utilities.exceptions import DecoratorCouldNotFindTargetMethod
from .._utilities.decorators import takes_arguments
from ..profiling.instrumentation import Profiler
from .. import benchmark as mb
from functools import wraps, partial
from uuid import uuid4


@takes_arguments
def collect_measurements(method, test_case_name, enabled=True):
    """
    This decorator can be used to gather performance statistical
    on a method.
    :param test_case_name: Used to attach a test case name to this decorator.
    :param method: The method that is being profiled
    :param enabled: If True will profile the method under test
    :return: The method functional output
    """
    # ---------------------------------------------------------------------
    # Setting up the profiling object so measurements an tracing can take place
    mb.test_case_name = test_case_name

    @wraps(method)
    def method_execution(*args, **kwargs):
        """
        An inner function that Will execute the method under test and enable the profiler.
        It will work together with the Results class to formulate a list containing dictionary
        that will store all metrics in a _database or csv file.
        :param args: The Arguments of the method under test
        :param kwargs: The key word arguments of the method under test
        :return: the methods results
        """
        # Measure and record method performance
        pf = Profiler()
        pf.profile_method_under_test(method, *args, **kwargs)

        # Extract and upload method performance statistics
        ProfilerStatisticsInterpreter(
            performance_statistics=pf.performance_statistics,
            total_response_time=pf.total_response_time,
            test_case_name=mb.test_case_name,
            connection_url=mb.database_connection_url,
            test_id=mb.test_id,
            method_name=method.__name__,
            sample_id=str(uuid4())[:8]
        )

        return pf.functional_output

    # ---------------------------------------------------------------------

    if method is None:
        return partial(method, test_case_name, enabled)

    elif callable(method) is not True:
        raise DecoratorCouldNotFindTargetMethod()

    else:
        # Return method under test with profiler tracers inplace.
        return method_execution
