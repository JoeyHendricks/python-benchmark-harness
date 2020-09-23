from QuickPotato.configuration.manager import options
from QuickPotato.utilities.exceptions import AgentCannotFindMethod
from QuickPotato.inspect.interpreters import TimeSpentInterpreter, SystemResourcesInterpreter
from QuickPotato.harness.testing import UnitPerformanceTest
from QuickPotato.inspect.debugger import Profiler
from functools import wraps, partial
import uuid

unit_performance_test = UnitPerformanceTest()


def performance_critical(method=None, enabled=True):
    """
    This decorator can be used to gather performance statistics
    on a method.
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
        if enabled and options.collect_performance_statistics:

            method_id = str(uuid.uuid1())
            pf = Profiler()
            pf.profile_method_under_test(method, *args, **kwargs)

            TimeSpentInterpreter(
                time_spent_statistics=pf.time_spent_statistics,
                database_name=unit_performance_test.test_case_name,
                test_id=unit_performance_test.current_test_id,
                method_name=method.__name__,
                method_id=method_id
            )

            SystemResourcesInterpreter(
                cpu_statistics=pf.system_resource_utilization_measurements,
                database_name=unit_performance_test.test_case_name,
                test_id=unit_performance_test.current_test_id,
                method_name=method.__name__,
                method_id=method_id
            )

            return pf.functional_output

        else:
            return method(*args, **kwargs)

    # ---------------------------------------------------------------------

    if method is None:
        return partial(performance_critical, enabled=enabled)

    elif callable(method) is not True:
        AgentCannotFindMethod()

    else:
        # Execute the method under test
        output = method_execution

        return output
