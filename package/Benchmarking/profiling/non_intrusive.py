from ..statistical.verification import check_max_boundary, check_min_boundary, check_letter_rank_boundary
from ..profiling.interpreters import ProfilerStatisticsInterpreter
from ..statistical.heuristics import StatisticalDistanceTest
from ..profiling.instrumentation import Profiler
from ..statistical.measurements import Statistics
from .._utilities.decorators import verify_method_annotations
from .._database.collection import Crud
from multiprocessing import Process
from datetime import datetime
from uuid import uuid4
import warnings
import time


class Benchmark(Crud):

    def __init__(self):
        super(Benchmark, self).__init__()

    def _execute_code_under_test(self, method: object, arguments=None, iteration=1, pacing=0) -> None:
        """

        :return:
        """
        # Iterations per test
        for _ in range(0, iteration):

            # Pacing in between actions.
            time.sleep(pacing)

            # Run method and profile it
            pf = Profiler()
            if arguments is None:
                pf.profile_method_under_test(method)
            else:
                pf.profile_method_under_test(method, *arguments)

            # Wrangle data into format and upload it to _database
            ProfilerStatisticsInterpreter(
                performance_statistics=pf.performance_statistics,
                total_response_time=pf.total_response_time,
                connection_url=self.database_connection_url,
                test_case_name=self.test_case_name,
                test_id=self.test_id,
                method_name=method.__name__,
                sample_id=str(uuid4())[:8]
            )

    @property
    def benchmark_statistics(self) -> Statistics:
        """
        All of the performance measurements that are collected by the benchmark.

        Returns
        -------
            A statistical object that contains all benchmark measurements.
        """
        response_times = self.select_benchmark_profiled_method_cumulative_latency(
            url=self.database_connection_url,
            tcn=self.test_case_name,
            test_id=self.test_id
        )
        return Statistics(
            measurements=response_times
        )

    @property
    def baseline_statistics(self) -> Statistics:
        """
        All of the performance measurements that are collected by the baseline.

        Returns
        -------
            A statistical object that contains all baseline measurements.
        """
        response_times = self.select_benchmark_profiled_method_cumulative_latency(
            url=self.database_connection_url,
            tcn=self.test_case_name,
            test_id=self.baseline_test_id
        )
        return Statistics(
            measurements=response_times
        )

    @property
    def regression(self) -> StatisticalDistanceTest:
        """

        :return:
        """
        return StatisticalDistanceTest(
            population_a=self.baseline_statistics.raw_data,
            population_b=self.benchmark_statistics.raw_data,
        )

    @property
    def test_case_name(self) -> str:
        """

        :return:
        """
        if "test_case_name" in self.__dict__:

            return self.__dict__["test_case_name"]

        else:
            return "default"

    @property
    def test_id(self) -> float or None:
        """

        :return:
        """
        if "test_id" in self.__dict__:

            return self.__dict__["test_id"]

        else:
            return None

    @property
    def baseline_test_id(self) -> float or None:
        """

        :return:
        """
        if "baseline_test_id" in self.__dict__:

            return self.__dict__["baseline_test_id"]

        else:
            return None

    @property
    def database_connection_url(self) -> str:
        """

        :return:
        """
        if "database_connection_url" not in self.__dict__:
            return self._create_default_db_url()

        else:
            return self.__dict__["database_connection_url"]

    @test_id.setter
    def test_id(self, value: float):
        """

        """
        self.__dict__["test_id"] = value

    @baseline_test_id.setter
    def baseline_test_id(self, value: float):
        """

        """
        self.__dict__["baseline_test_id"] = value

    @test_case_name.setter
    def test_case_name(self, value: str) -> None:
        """
        Will update the test case name with the provided value.
        When the test case name is changed by a performance unit test.
        The following automatic action will be performed:

            - Create the necessary tables in target _database.
            - Find the previous test id
            - Generate the current test id

        :param value: The new test case name defined by the user.
        """
        # create tables in database where benchmark needs to save statistics.
        self._verify_and_create_relevant_tables_in_database(
            url=self.database_connection_url,
            tcn=value
        )
        self.__dict__["test_case_name"] = value

        # reset the performance test identifying variables.
        benchmarks = self.select_benchmarks_with_statistics(
            url=self.database_connection_url,
            tcn=value,
            number=1
        )
        self.baseline_test_id = benchmarks[0] if len(benchmarks) > 0 else None
        self.test_id = datetime.now().timestamp()

    @database_connection_url.setter
    def database_connection_url(self, value: str) -> None:
        """

        :param value:
        :return:
        """
        self.__dict__['database_connection_url'] = value

    @verify_method_annotations
    def verify_boundaries(self, boundaries: list) -> bool or None:
        """

        :param boundaries:
        :return:
        """
        self.__dict__['boundary_verification_results'] = []
        for boundary in boundaries:
            self.__dict__['boundary_verification_results'].append(
                {
                    "uuid": str(uuid4()),
                    "test_id": self.test_id,
                    "boundary_name": boundary["name"],
                    "value": boundary["value"],
                    "minimum_boundary": boundary["minimum"],
                    "maximum_boundary": boundary["maximum"],
                    "minimum_verification_results": check_min_boundary(
                        boundary["value"],
                        boundary["minimum"]
                    ),
                    "maximum_verification_results": check_max_boundary(
                        boundary["value"],
                        boundary["maximum"]
                    ),
                }
            )

        # Upload test evidence
        self.bulk_insert(
            connection_url=self.database_connection_url,
            table=self.boundary_test_report_model(self.test_case_name),
            payload=self.__dict__['boundary_verification_results']
        )

        # Verification
        if len(self.__dict__['boundary_verification_results']) == 0:
            warnings.warn("Warning no test have been executed against the benchmark")
            return None

        elif False in self.__dict__['boundary_verification_results']:
            return False

        else:
            return True

    @verify_method_annotations
    def compare_measurements(self, instructions: dict) -> bool:
        """

        :param instructions:
        :return:
        """
        self.__dict__['comparison_results'] = [
            {
                "uuid": str(uuid4()),
                "test_id": self.test_id,
                "critical_letter_rank": instructions["critical_letter_rank"],
                "observed_letter_rank": self.regression.letter_rank,
                "critical_score": instructions["critical_score"],
                "observed_score": self.regression.score,
                "letter_rank_comparison_result": check_letter_rank_boundary(
                    instructions["critical_letter_rank"],
                    self.regression.letter_rank
                ),
                "score_comparison_result": check_min_boundary(
                    self.regression.score,
                    instructions["critical_score"]
                )
            }
        ]
        self.bulk_insert(
            connection_url=self.database_connection_url,
            table=self.compare_test_report_model(self.test_case_name),
            payload=self.__dict__['comparison_results']
        )
        return False if False in self.__dict__['comparison_results'] else True

    def run(self, method, arguments=None, iteration=1, pacing=0, processes=0):
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
