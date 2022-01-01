import random
import string
from functools import wraps, partial
from QuickPotato import performance_test as pt
from QuickPotato.configuration.management import options
from QuickPotato.benchmarking.code_instrumentation import Profiler
from QuickPotato.benchmarking.profiler_interpreter import ProfilerStatisticsInterpreter
from QuickPotato.utilities.exceptions import CouchPotatoCannotFindMethod
from QuickPotato.utilities.defaults import default_test_case_name, default_database_name


def performance_breakpoint(method=None, enabled=True, test_case_name=default_test_case_name,
                           database_name=default_database_name, test_id=None):
    """
    This decorator can be used to gather performance statistical
    on a method.
    :param test_id: Used to overwrite the automatically generated test id with a custom one.
    :param database_name: the name of the database that this test case uses.
    :param test_case_name: Used to attach a test case name to this decorator.
    :param method: The method that is being profiled
    :param enabled: If True will profile the method under test
    :return: The method output
    """
    # ---------------------------------------------------------------------

    @wraps(method)
    def method_execution(*args, **kwargs):
        """
        An inner function that Will execute the method under test and enable the profiler.
        It will work together with the Results class to formulate a list containing dictionary
        that will store all metrics in a database or csv file.
        :param args: The Arguments of the method under test
        :param kwargs: The key word arguments of the method under test
        :return: the methods results
        """
        if enabled and options.enable_intrusive_profiling:

            sample_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            pf = Profiler()
            pf.profile_method_under_test(method, *args, **kwargs)

            pt.database_connection_url = database_name
            pt.test_case_name = test_case_name

            ProfilerStatisticsInterpreter(
                performance_statistics=pf.performance_statistics,
                total_response_time=pf.total_response_time,
                test_case_name=pt.test_case_name,
                database_name=pt.database_connection_url,
                test_id=pt.current_test_id if test_id is None else test_id,
                method_name=method.__name__,
                sample_id=sample_id
            )

            return pf.functional_output

        else:
            return method(*args, **kwargs)

    # ---------------------------------------------------------------------

    if method is None:
        return partial(
            performance_breakpoint,
            enabled=enabled,
            test_case_name=test_case_name,
            test_id=test_id,
            database_name=database_name
        )

    elif callable(method) is not True:
        raise CouchPotatoCannotFindMethod()

    else:
        # Execute the method under test
        output = method_execution
        return output
