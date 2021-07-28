from QuickPotato import performance_test as pt
from QuickPotato.configuration.management import options
from examples.non_intrusive_example_code import FancyCode
import unittest


class TestPerformance(unittest.TestCase):

    def setUp(self):
        """
        Disable the selection of failed or untested test results.
        This will make sure QuickPotato will only compare you tests against a valid baseline.
        """
        options.enable_policy_to_filter_out_invalid_test_ids = False

    def tearDown(self):
        """
        Enabling the selection of failed or untested test results.
        We enable this setting after the test so it will not bother you when quick profiling.
        """
        options.enable_policy_to_filter_out_invalid_test_ids = True

    def test_performance_of_method(self):
        """
        Your performance test.
        """
        # Create a test case
        pt.test_case_name = "test_performance"  # <-- Define test case name

        # Defining the boundaries
        pt.max_and_min_boundary_for_average = {"max": 10, "min": 0.001}

        # Execute your code in a non-intrusive way
        pt.measure_method_performance(
            method=FancyCode().say_my_name_and_more,  # <-- The Method which you want to test.
            arguments=["joey hendricks"],  # <-- Your arguments go here.
            iteration=10,  # <-- The number of times you want to execute this method.
            pacing=0  # <-- How much seconds you want to wait between iterations.
        )

        # Pass or fail the performance test
        self.assertTrue(pt.verify_benchmark_against_previous_baseline())
        self.assertTrue(pt.verify_benchmark_against_set_boundaries())
