from QuickPotato.statistical.verification import check_max_boundary_of_measurement, check_min_boundary_of_measurement
from QuickPotato.configuration.settings import Boundaries, RegressionSettings
from QuickPotato.configuration.management import options
from QuickPotato.statistical.hypothesis_tests import TTest
from QuickPotato.benchmarking.metrics import Metrics
from QuickPotato.database.collection import Crud
from QuickPotato.benchmarking.metrics import Statistics
from QuickPotato.profiling.instrumentation import Profiler
from QuickPotato.profiling.interpreters import ProfilerStatisticsInterpreter
from datetime import datetime
from multiprocessing import Process
from tempfile import gettempdir
import warnings
import string
import random
import time


class PerformanceTest(Crud, Boundaries, Metrics, RegressionSettings):

    def __init__(self):
        Crud.__init__(self)
        Boundaries.__init__(self)
        Metrics.__init__(self)
        RegressionSettings.__init__(self)

        self.current_test_id = None
        self.previous_test_id = None

        self._test_case_name = "ProfilerStatistics"
        self._url = None

    @property
    def database_connection_url(self):
        """

        :return:
        """
        if self._url is None:
            temp_directory = gettempdir()
            separator = "\\" if '\\' in gettempdir() else "/"
            return "sqlite:///" + temp_directory + separator + self._test_case_name + ".db"

        else:
            return self._url

    @database_connection_url.setter
    def database_connection_url(self, value):
        """

        :param value:
        :return:
        """
        self._url = value

    @property
    def benchmark_measurements(self):
        """
        All of the performance measurements that are collected by the benchmark.

        Returns
        -------
            A statistical object that contains all benchmark measurements.
        """
        return Statistics(test_id=self.current_test_id, database_name=self.database_connection_url)

    @property
    def baseline_measurements(self):
        """
        All of the performance measurements that are collected by the baseline.

        Returns
        -------
            A statistical object that contains all baseline measurements.
        """
        return Statistics(test_id=self.previous_test_id, database_name=self.database_connection_url)

    @database_connection_url.setter
    def database_connection_url(self, value):
        """

        :param value:
        :return:
        """
        self.database_connection_url = value

    @property
    def test_case_name(self):
        """
        The test case name that has been defined in the unit load test.

        Raises
        -------
            AgentCannotFindTestCase If no test case is found
        """
        return self._test_case_name

    @test_case_name.setter
    def test_case_name(self, value: str) -> None:
        """
        Will update the test case name with the provided value.
        When the test case name is changed by a performance unit test.
        The following automatic action will be performed:

            - Create the necessary tables in target database.
            - Find the previous test id
            - Generate the current test id

        :param value: The new test case name defined by the user.
        """
        self._verify_and_create_relevant_tables_in_database(
            url=self.database_connection_url,
            tcn=value
        )
        self._test_case_name = value
        self._reset_performance_test(value)

    def verify_benchmark_against_set_boundaries(self):
        """

        :return:
        """
        results = self._check_breach_benchmark_defined_boundaries()
        return results

    def verify_benchmark_against_previous_baseline(self):
        """

        :return:
        """
        results = self._check_difference_between_baseline_benchmark()
        return results

    def _execute_code_under_test(self, method, arguments=None, iteration=1, pacing=0):
        """

        :return:
        """
        # Iterations per test
        for _ in range(0, iteration):

            # Pacing in between actions.
            time.sleep(pacing)

            # Random ID.
            sample_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

            # Run method and profile it
            pf = Profiler()
            if arguments is None:
                pf.profile_method_under_test(method)
            else:
                pf.profile_method_under_test(method, *arguments)

            # Wrangle data into format and upload it to database
            ProfilerStatisticsInterpreter(
                performance_statistics=pf.performance_statistics,
                total_response_time=pf.total_response_time,
                connection_url=self.database_connection_url,
                test_case_name=self.test_case_name,
                test_id=self.current_test_id,
                method_name=method.__name__,
                sample_id=sample_id
            )

    def measure_method_performance(self, method, arguments=None, iteration=1, pacing=0, processes=0):
        """

        :param method:
        :param arguments:
        :param iteration:
        :param pacing:
        :param processes:
        :return:
        """
        if __name__ == "__main__" and processes > 0:
            for _ in range(0, processes):
                Process(
                    name=f"worker-{_}",
                    target=self._execute_code_under_test,
                    kwargs={
                        "method": method,
                        "arguments": arguments,
                        "iteration": iteration,
                        "pacing": pacing
                    }
                ).start()

        else:
            self._execute_code_under_test(
                method,
                arguments,
                iteration,
                pacing,
            )

    def _reset_performance_test(self, test_case_name):
        """

        :param test_case_name:
        :return:
        """
        self.previous_test_id = self.select_benchmarks_tests_with_statistics(
            url=self.database_connection_url,
            tcn=test_case_name,
            number=1
        )[0]
        self.current_test_id = datetime.now().timestamp()

    def _inspect_test_results(self, results):
        """
        Will verify the test results and will give an appropriate output
        and  warning message.

        Returns
        -------
            - True = Test Passed
            - False = Test Failed
            _ None = No test performed (throws an warning message)
        """
        if len(results) == 0:
            warnings.warn("Warning no test have been executed against the benchmark")
            return True

        elif False in results:
            return False

        else:
            return True

    def _check_breach_benchmark_defined_boundaries(self):
        """
        This method will validate how well the benchmark will hold up to the
        set threshold in the service level agreement.

        Returns
        -------
            True if the test passes and False if it False
        """
        results = []
        self._collect_measurements(test_id=self.current_test_id, database_name=self.database_connection_url)
        for boundary_key, measurements_key in zip(self.boundary_policy, self.threshold_measurements):
            if self.boundary_policy[boundary_key]["max"] is not None:
                results.append(
                    check_max_boundary_of_measurement(
                        boundary=self.boundary_policy[boundary_key]["max"],
                        value=self.threshold_measurements[measurements_key]())
                )
            if self.boundary_policy[boundary_key]["min"] is not None:
                results.append(
                    check_min_boundary_of_measurement(
                        boundary=self.boundary_policy[boundary_key]["min"],
                        value=self.threshold_measurements[measurements_key]())
                )
        return self._inspect_test_results(results)

    def _check_difference_between_baseline_benchmark(self):
        """
        Will test the benchmark against the baseline.
        The following statistical tests are performed in this method:

            - T test

        Returns
        -------
            True = Test Passed
            False = Test Failed
            None = No test performed
        """
        # Validate if there is a proper baseline and benchmark present
        t_test = TTest(
            test_id=self.current_test_id,
            test_case_name=self._test_case_name,
            database_name=self.database_connection_url,
            baseline_measurements=self.baseline_measurements.response_times(),
            benchmark_measurements=self.benchmark_measurements.response_times()
        )
        print(t_test.results)
