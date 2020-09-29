from QuickPotato.configuration.settings import Boundaries, RegressionSettings
from QuickPotato.utilities.templates import default_test_case_name
from QuickPotato.statistics.hypothesis_tests import TTest, FTest
from QuickPotato.harness.results import Measurements
from QuickPotato.database.actions import DatabaseActions
from QuickPotato.statistics.verification import *
from QuickPotato.harness.results import RawData
import string
import random


class UnitPerformanceTest(DatabaseActions, Boundaries, Measurements, RegressionSettings):

    def __init__(self):

        DatabaseActions.__init__(self)
        Boundaries.__init__(self)
        RegressionSettings.__init__(self)
        Measurements.__init__(self)

        self._current_test_id = None
        self._previous_test_id = None
        self._test_case_name = None
        self._silence_warning_messages = False
        self._outside_of_unit_performance_test = True

    @property
    def current_test_id(self):
        return self._current_test_id

    @property
    def silence_warning_messages(self):
        return self._silence_warning_messages

    @silence_warning_messages.setter
    def silence_warning_messages(self, value):
        self._silence_warning_messages = value

    @property
    def benchmark_measurements(self):
        """
        All of the performance measurements that are collected by the benchmark.

        Returns
        -------
            A raw data object that contains all benchmark measurements.
        """
        return RawData(test_id=self.current_test_id, database_name=self._test_case_name)

    @property
    def baseline_measurements(self):
        """
        All of the performance measurements that are collected by the baseline.

        Returns
        -------
            A raw data object that contains all baseline measurements.
        """
        return RawData(test_id=self._previous_test_id, database_name=self._test_case_name)

    @property
    def test_case_name(self):
        """
        The test case name that has been defined in the unit load test.

        Raises
        -------
            AgentCannotFindTestCase If no test case is found
        """
        if self._outside_of_unit_performance_test is False:
            return self._test_case_name

        else:
            self._create_and_populate_test_case_database(default_test_case_name)
            self._current_test_id = "collected_outside_unit_performance_test"
            return default_test_case_name

    @test_case_name.setter
    def test_case_name(self, value):
        """
        Will update the test case name with the provided value.

        When the test case name is changed by a performance unit test.
        The following automatic action will be performed:

            - Create the database schema and tables.
            - Find the previous test id
            - Create the current test id

        Parameters
        ----------
        value
            the new value of the test case name that will
            be defined by the developer.
        """
        self._create_and_populate_test_case_database(value)
        self._outside_of_unit_performance_test = False

        # Refresh Test ID's
        self._reset_unit_performance_test(database_name=value)
        self._test_case_name = value

    def _create_and_populate_test_case_database(self, database):
        """
        """
        self.spawn_results_database(database)
        self.spawn_time_spent_table(database)
        self.spawn_system_resources_table(database)
        self.spawn_boundaries_test_report_table(database)
        self.spawn_regression_test_report_table(database)
        self.enforce_test_result_retention_policy(database)

    def _reset_unit_performance_test(self, database_name):
        """
        The method will reset the unit load test class to it original state.

        Parameters
        ----------
        database_name
            The name of the database also known as the test case name
        Returns
        -------
            Will return True on success
        """
        self._previous_test_id = str(self.select_previous_test_id(database_name=database_name))
        self._current_test_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    def _inspect_benchmark_and_baseline(self):
        """
        Will verify if the benchmark and baseline result can be used in a validation.

        Returns
        -------
            Will return True if the test ids do not match and do not contain a None type.
            Will return False if the test ids do not match the above requirements.
            Will return None if the sum of both the baseline and benchmark equal to zero
        """
        if self._current_test_id == "None" or self._previous_test_id == "None":
            # Test case is empty
            return False

        elif self._current_test_id == self._previous_test_id:
            # Test Cases are the same
            return False

        else:
            # Two different test cases regression analysis can be done
            return True

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
            if self._silence_warning_messages is False:
                print("Warning no test have been executed against the benchmark")
            return None

        elif False in results:
            return False

        else:
            return True

    def verify_if_benchmark_does_not_breach_defined_boundaries(self):
        """
        This method will validate how well the benchmark will hold up to the
        set threshold in the service level agreement.

        Returns
        -------
            True if the test passes and False if it False
        """
        results = []
        self._collect_measurements(test_id=self.current_test_id, database_name=self._test_case_name)
        for boundary_key, measurements_key in zip(self.boundary_policy,
                                                  self.threshold_measurements):
            if self.boundary_policy[boundary_key]["max"] is not None:
                results.append(
                    validate_max_boundary_of_measurements(
                        test_id=self.current_test_id,
                        test_case_name=self._test_case_name,
                        validation_name="validate_max_boundary_for_" + measurements_key,
                        boundary=self.boundary_policy[boundary_key]["max"],
                        value=self.threshold_measurements[measurements_key]())
                )

            if self.boundary_policy[boundary_key]["min"] is not None:
                results.append(
                    validate_min_boundary_of_measurements(
                        test_id=self.current_test_id,
                        test_case_name=self._test_case_name,
                        validation_name="validate_min_boundary_for_" + measurements_key,
                        boundary=self.boundary_policy[boundary_key]["min"],
                        value=self.threshold_measurements[measurements_key]())
                )

        return self._inspect_test_results(results)

    def verify_that_there_is_no_change_between_the_baseline_and_benchmark(self):
        """
        Will test the benchmark against the baseline.
        The following statistical tests are performed in this method:

            - T test
            - F test

        Returns
        -------
            True = Test Passed
            False = Test Failed
            None = No test performed
        """
        # Validate if there is a proper baseline and benchmark present
        if self._inspect_benchmark_and_baseline():
            results = []

            if self.regression_setting_perform_t_test:
                t_test = TTest(
                    test_id=self.current_test_id,
                    test_case_name=self._test_case_name,
                    baseline_measurements=self.baseline_measurements.response_times(),
                    benchmark_measurements=self.benchmark_measurements.response_times()
                )
                results.append(t_test.results)

            if self.regression_setting_perform_f_test:
                f_test = FTest(
                    test_id=self.current_test_id,
                    test_case_name=self._test_case_name,
                    baseline_measurements=self.baseline_measurements.response_times(),
                    benchmark_measurements=self.benchmark_measurements.response_times()
                )
                results.append(f_test.results)

            return self._inspect_test_results(results)

        elif self._inspect_benchmark_and_baseline() is None:

            return True

        else:
            if self._silence_warning_messages is False:
                print("Warning no baseline found so no regression test performed")
            return None
