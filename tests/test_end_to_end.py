from QuickPotato.inspect.intrusive import unit_performance_test
from QuickPotato.database.management import DatabaseManager
from tests.stubs import *
import unittest


class TestBoundariesEndToEnd(unittest.TestCase):

    SAMPLE_SIZE = 10
    DELETE_TEMPORARY_DATABASE_AFTER_USE = True
    TEMPORARY_UNIT_TEST_DATABASE_NAME = "quick_potato_unit_test_database"

    def tearDown(self):
        if self.DELETE_TEMPORARY_DATABASE_AFTER_USE is True:
            database_manager = DatabaseManager()
            database_manager.delete_result_database(database_name=self.TEMPORARY_UNIT_TEST_DATABASE_NAME)

    def test_output_with_no_breached_boundary(self):

        # Define Test Case
        upt = unit_performance_test
        upt.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
        upt.max_and_min_boundary_for_average = {"max": 1, "min": 0.001}

        # Execute method under test
        for _ in range(0, self.SAMPLE_SIZE):
            slow_method()

        # Analyse profiled results
        results = upt.verify_if_benchmark_does_not_breach_defined_boundaries()

        self.assertTrue(results)

    def test_output_with_breached_boundary(self):

        # Define Test Case
        upt = unit_performance_test
        upt.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
        upt.max_and_min_boundary_for_average = {"max": 0.010, "min": 0.001}

        # Execute method under test
        for _ in range(0, self.SAMPLE_SIZE):
            slow_method()

        # Analyse profiled results
        results = upt.verify_if_benchmark_does_not_breach_defined_boundaries()

        self.assertFalse(results)

    def test_output_with_all_boundaries_enabled(self):

        # Define Test Case
        upt = unit_performance_test
        upt.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
        upt.max_and_min_boundary_for_average = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_largest_outlier = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_5th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_10th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_15th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_20th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_25th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_30th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_35th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_40th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_45th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_50th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_55th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_60th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_65th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_70th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_75th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_80th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_85th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_90th = {"max": 1, "min": 0.001}
        upt.max_and_min_boundary_for_percentile_95th = {"max": 1, "min": 0.001}

        # Execute method under test
        for _ in range(0, self.SAMPLE_SIZE):
            slow_method()

        # Analyse profiled results
        results = upt.verify_if_benchmark_does_not_breach_defined_boundaries()

        self.assertTrue(results)


class TestRegressionEndToEnd(unittest.TestCase):

    DEFAULT_SAMPLE_SIZE = 10
    DELETE_TEMPORARY_DATABASE_AFTER_USE = True
    TEMPORARY_UNIT_TEST_DATABASE_NAME = "quick_potato_unit_test_database"

    def set_baseline(self, slowdown):
        # Creating a default_baseline
        upt = unit_performance_test
        upt.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
        for _ in range(0, self.DEFAULT_SAMPLE_SIZE):
            if slowdown is True:
                slow_method()
            else:
                fast_method()

    def tearDown(self):
        if self.DELETE_TEMPORARY_DATABASE_AFTER_USE is True:
            database_manager = DatabaseManager()
            database_manager.delete_result_database(database_name=self.TEMPORARY_UNIT_TEST_DATABASE_NAME)

    def test_slow_benchmark_against_fast_baseline(self):

        # Creating a fast baseline
        self.set_baseline(slowdown=False)

        # Define Test Case
        upt = unit_performance_test
        upt.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
        upt.regression_setting_perform_f_test = True
        upt.regression_setting_perform_t_test = True

        # Execute method under test
        for _ in range(0, self.DEFAULT_SAMPLE_SIZE):
            slow_method()

        # Analyse profiled results
        results = upt.verify_that_there_is_no_change_between_the_baseline_benchmark()
        self.assertFalse(results)

    def test_fast_benchmark_against_slow_baseline(self):

        # Creating a fast baseline
        self.set_baseline(slowdown=True)

        # Define Test Case
        upt = unit_performance_test
        upt.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
        upt.regression_setting_perform_f_test = True
        upt.regression_setting_perform_t_test = True

        # Execute method under test
        for _ in range(0, self.DEFAULT_SAMPLE_SIZE):
            fast_method()

        # Analyse profiled results
        results = upt.verify_that_there_is_no_change_between_the_baseline_benchmark()
        self.assertFalse(results)

    def test_baseline_against_benchmark_with_no_regression(self):

        # Creating a fast baseline
        self.set_baseline(slowdown=False)

        # Define Test Case
        upt = unit_performance_test
        upt.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
        upt.regression_setting_perform_f_test = True
        upt.regression_setting_perform_t_test = True

        # Execute method under test
        for _ in range(0, self.DEFAULT_SAMPLE_SIZE):
            fast_method()

        # Analyse profiled results
        results = upt.verify_that_there_is_no_change_between_the_baseline_benchmark()
        self.assertTrue(results)



