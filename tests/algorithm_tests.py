from QuickPotato.inspect.intrusive import unit_performance_test
from QuickPotato.database.management import DatabaseManager
from tests.stubs import *
import unittest

delete_test_database = False


class TestMechanisms(unittest.TestCase):
    """
    A QuickPotato test set that will test the intrusive way of validating your code.
    See the documentation for more information about the intrusive code inspect and testing.
    """

    TEMPORARY_UNIT_TEST_DATABASE_NAME = "quick_potato_unit_test_database"

    def tearDown(self):
        """
        Will delete the database used by the unit tests.
        """
        if delete_test_database is True:
            database_manager = DatabaseManager()
            database_manager.delete_result_database(database_name=self.TEMPORARY_UNIT_TEST_DATABASE_NAME)

    def test_threshold_mechanism(self):
        """
        Within this test we verify if it is possible to use the threshold mechanism.

        It is possible to use this mechanism to validate if the performance of your code
        stays between two boundaries. It possible to load in different profiles of threshold
        depending on the test environment you are using.

        See the full documentation of all supported boundaries.
        """
        unit_performance_test.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
        unit_performance_test.max_and_min_boundary_for_average = {"max": 1, "min": None}

        # Execute method under test
        output = slow_method()

        test_results = unit_performance_test.analyse_benchmark_against_defined_boundaries()

        self.assertTrue(test_results)
        self.assertEqual(first=output, second=36306)

    def test_regression_mechanism(self):
        """
        Within this test we verify if it is possible to use the regression mechanism.
        It is possible to use this mechanism to automatically verify if your code
        change has led to a performance degradation.

        This done with an Students T test to validate if there is any statistical
        difference between the two unit performance tests.
        """
        database_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME

        def baseline():
            unit_performance_test.test_case_name = database_name

            # Execute method under test 10 times
            for _ in range(0, 10):
                slow_method()

            return True

        def benchmark():
            unit_performance_test.test_case_name = database_name
            unit_performance_test.regression_setting_perform_f_test = True
            unit_performance_test.regression_setting_perform_t_test = True

            # Execute method under test 10 times
            for _ in range(0, 10):
                fast_method()

            return unit_performance_test.analyse_benchmark_against_baseline_for_regression()

        # Set Slow Baseline
        baseline()

        # Test Faster Benchmark
        self.assertFalse(benchmark())


