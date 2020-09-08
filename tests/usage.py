from QuickPotato.inspect.intrusive import unit_performance_test
from QuickPotato.database.management import DatabaseManager
from tests.stubs import *
import unittest

delete_test_database = True


class TestFirstUse(unittest.TestCase):
    """
    A QuickPotato test set that will test the first use mechanisms.
    See the documentation for support on the topic.
    """

    TEMPORARY_UNIT_TEST_DATABASE_NAME = "quick_potato_unit_test_database"

    def tearDown(self):
        """
        Will delete the database used by the unit tests.
        """
        if delete_test_database is True:
            database_manager = DatabaseManager()
            database_manager.delete_result_database(database_name=self.TEMPORARY_UNIT_TEST_DATABASE_NAME)

    def test_first_use_automated_regression_validation(self):
        """
        The first time a unit test will be executed there will be no baseline
        to compare the benchmark against this will resolve in an error.
        """
        unit_performance_test.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
        unit_performance_test.max_and_min_boundary_for_average = {"max": 1, "min": None}
        unit_performance_test.silence_warning_messages = True

        for _ in range(0, 10):
            fast_method()

        output_regression_validation = unit_performance_test.analyse_benchmark_against_baseline_for_regression()
        output_threshold_validation = unit_performance_test.analyse_benchmark_against_defined_boundaries()

        self.assertIsNone(output_regression_validation)
        self.assertTrue(output_threshold_validation)

    def test_variable_usage_of_unit_performance_test_object(self):
        """

        Returns
        -------

        """
        upt = unit_performance_test
        upt.test_case_name = self.TEMPORARY_UNIT_TEST_DATABASE_NAME
        upt.max_and_min_boundary_for_average = {"max": 1, "min": None}
        upt.silence_warning_messages = True

        for _ in range(0, 10):
            fast_method()

        output_regression_validation = upt.analyse_benchmark_against_baseline_for_regression()
        output_threshold_validation = upt.analyse_benchmark_against_defined_boundaries()

        self.assertIsNone(output_regression_validation)
        self.assertTrue(output_threshold_validation)
