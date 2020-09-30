from QuickPotato.inspect.intrusive import unit_performance_test as upt
from QuickPotato.database.management import DatabaseManager
from QuickPotato.configuration.manager import options
from demo.example_code import *
import unittest


class TestStability(unittest.TestCase):

    SAMPLE_SIZE = 10
    DELETE_TEMPORARY_DATABASE_AFTER_USE = False
    TEMPORARY_UNIT_TEST_DATABASE_NAME = "quick_potato_regression_test_database"

    def set_baseline(self):
        # Creating a default_baseline
        upt.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
        upt.regression_setting_perform_t_test = True

        for _ in range(0, self.SAMPLE_SIZE):
            fast_method()

        upt.verify_that_there_is_no_change_between_the_baseline_and_benchmark()

    def setUp(self):
        options.enable_intrusive_profiling = True
        self.set_baseline()

    def tearDown(self):
        if self.DELETE_TEMPORARY_DATABASE_AFTER_USE is True:
            database_manager = DatabaseManager()
            database_manager.delete_result_database(database_name=self.TEMPORARY_UNIT_TEST_DATABASE_NAME)

    def test_t_test_statistical_for_accuracy(self):

        results = []

        for _ in range(0, 100):
            # Define Test Case
            upt.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
            upt.regression_setting_perform_t_test = True

            # Execute method under test
            for _ in range(0, self.SAMPLE_SIZE):
                fast_method()

            # Analyse profiled results
            output = upt.verify_that_there_is_no_change_between_the_baseline_and_benchmark()
            if output:
                print("-------------------------")
                print(f"OK benchmark measurements - {sum(upt.benchmark_measurements.response_times())} - "
                      f"{upt.benchmark_measurements.response_times()}")
                print(f"OK baseline  measurements - {sum(upt.baseline_measurements.response_times())} - "
                      f"{upt.baseline_measurements.response_times()}")
                print("-------------------------")

            else:
                print("-------------------------")
                print(f"NOK benchmark measurements - {sum(upt.benchmark_measurements.response_times())} - "
                      f"{upt.benchmark_measurements.response_times()}")
                print(f"NOK baseline  measurements - {sum(upt.baseline_measurements.response_times())} - "
                      f"{upt.baseline_measurements.response_times()}")
                print("-------------------------")
            results.append(output)

        for test in results:
            self.assertTrue(test)

    def test_f_test_statistical_for__accuracy(self):

        results = []

        for _ in range(0, 100):
            # Define Test Case
            upt.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
            upt.regression_setting_perform_f_test = True

            # Execute method under test
            for _ in range(0, self.SAMPLE_SIZE):
                fast_method()

            # Analyse profiled results
            output = upt.verify_that_there_is_no_change_between_the_baseline_and_benchmark()
            if output:
                print("-------------------------")
                print(f"OK benchmark measurements - {sum(upt.benchmark_measurements.response_times())} - "
                      f"{upt.benchmark_measurements.response_times()}")
                print(f"OK baseline  measurements - {sum(upt.baseline_measurements.response_times())} - "
                      f"{upt.baseline_measurements.response_times()}")
                print("-------------------------")

            else:
                print("-------------------------")
                print(f"NOK benchmark measurements - {sum(upt.benchmark_measurements.response_times())} - "
                      f"{upt.benchmark_measurements.response_times()}")
                print(f"NOK baseline  measurements - {sum(upt.baseline_measurements.response_times())} - "
                      f"{upt.baseline_measurements.response_times()}")
                print("-------------------------")
            results.append(output)

        for test in results:
            self.assertTrue(test)

    def test_both_t_test_and_f_test_for_statistical_accuracy(self):

        results = []

        for _ in range(0, 100):
            # Define Test Case
            upt.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
            upt.regression_setting_perform_t_test = True
            upt.regression_setting_perform_f_test = True

            # Execute method under test
            for _ in range(0, self.SAMPLE_SIZE):
                fast_method()

            # Analyse profiled results
            output = upt.verify_that_there_is_no_change_between_the_baseline_and_benchmark()
            if output:
                print("-------------------------")
                print(f"OK benchmark measurements - {sum(upt.benchmark_measurements.response_times())} - "
                      f"{upt.benchmark_measurements.response_times()}")
                print(f"OK baseline  measurements - {sum(upt.baseline_measurements.response_times())} - "
                      f"{upt.baseline_measurements.response_times()}")
                print("-------------------------")

            else:
                print("-------------------------")
                print(f"NOK benchmark measurements - {sum(upt.benchmark_measurements.response_times())} - "
                      f"{upt.benchmark_measurements.response_times()}")
                print(f"NOK baseline  measurements - {sum(upt.baseline_measurements.response_times())} - "
                      f"{upt.baseline_measurements.response_times()}")
                print("-------------------------")
            results.append(output)

        for test in results:
            self.assertTrue(test)
