from QuickPotato.statistical.verification import check_max_boundary_of_measurement, check_min_boundary_of_measurement
from QuickPotato.benchmarking.c_profiler_interpreter import ProfilerStatisticsInterpreter
from QuickPotato.benchmarking.code_instrumentation import Profiler
from QuickPotato.statistical.measurements import Statistics
from QuickPotato.statistical.hypothesis_tests import TTest
from QuickPotato.database.collection import Crud
from multiprocessing import Process
from datetime import datetime
import warnings
import string
import random
import time


class MicroBenchmark(Crud):

    def __init__(self):
        Crud.__init__(self)

        # Test Meta variables
        self.current_test_id = None
        self.previous_test_id = None
        self._test_case_name = "Default"
        self._url = None

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

    @property
    def database_connection_url(self):
        """

        :return:
        """
        if self._url is None:
            return self._create_default_db_url()

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
    def benchmark_statistics(self):
        """
        All of the performance measurements that are collected by the benchmark.

        Returns
        -------
            A statistical object that contains all benchmark measurements.
        """
        response_times = self.select_benchmark_profiled_method_response_times(
            url=self.database_connection_url,
            tcn=self.test_case_name,
            test_id=self.current_test_id
        )
        return Statistics(
            measurements=response_times
        )

    @property
    def baseline_statistics(self):
        """
        All of the performance measurements that are collected by the baseline.

        Returns
        -------
            A statistical object that contains all baseline measurements.
        """
        response_times = self.select_benchmark_profiled_method_response_times(
            url=self.database_connection_url,
            tcn=self.test_case_name,
            test_id=self.previous_test_id
        )
        return Statistics(
            measurements=response_times
        )

    @staticmethod
    def verify_boundaries(boundaries: list) -> bool or None:
        """

        :return:
        """
        results = []
        for boundary in boundaries:
            results.append(
                {
                    "boundary_name": boundary["name"],
                    "value": boundary["value"],
                    "minimum_boundary": boundary["minimum"],
                    "maximum_boundary": boundary["maximum"],
                    "minimum_verification_results": check_min_boundary_of_measurement(
                        boundary["value"],
                        boundary["minimum"]
                    ),
                    "maximum_verification_results": check_max_boundary_of_measurement(
                        boundary["value"],
                        boundary["maximum"]
                    ),
                }
            )

        if len(results) == 0:
            warnings.warn("Warning no test have been executed against the benchmark")
            return None

        elif False in results:
            return False

        else:
            return True

    def compare(self):
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
        benchmarks = self.select_benchmarks_with_statistics(
            url=self.database_connection_url,
            tcn=test_case_name,
            number=1
        )
        self.previous_test_id = benchmarks[0] if len(benchmarks) > 0 else None
        self.current_test_id = datetime.now().timestamp()

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
            baseline_measurements=self.baseline_statistics.raw_data,
            benchmark_measurements=self.benchmark_statistics.raw_data
        )
        print(t_test.results)
