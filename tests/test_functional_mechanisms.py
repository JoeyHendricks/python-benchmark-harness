from tests.stubs import FancyCode
from package.Benchmarking import benchmark as mb
from package.Benchmarking.statistical.verification import check_letter_rank_boundary
import unittest
import re


class TestVerifications(unittest.TestCase):

    ITERATIONS = 10

    def setUp(self) -> None:
        """
        This function will be executed before the unit tests will
        start and will setup all of the prerequisites.
        """
        self._create_basic_baseline_in_unit_test_database()

    def _create_basic_baseline_in_unit_test_database(self):
        """
        Will create an stable baseline run in the database.
        """
        mb.test_case_name = "demo"
        mb.run(
            method=FancyCode().calculate_statistics_about_fancy_population,
            arguments=[],
            iteration=self.ITERATIONS,
            pacing=0,
        )

    def test_ranking_heuristic_on_code_with_no_change_and_no_regression(self):
        """
        This test is used to verify if the heuristic is ranking
        benchmark against baselines that does not change.

        The dummy code that is used in the code should not slow
        down or show an interesting amount of regression.
        So it should not rank below an A letter rank.
        """
        for _ in range(0, self.ITERATIONS):
            # Run a benchmark on our demo code.
            mb.test_case_name = "demo"
            mb.run(
                method=FancyCode().calculate_statistics_about_fancy_population,
                arguments=[],
                iteration=self.ITERATIONS,
                pacing=0,
            )
            # Verify if the benchmark meets the predefined criteria.
            self.assertTrue(
                check_letter_rank_boundary(
                    boundary_letter_rank="A",
                    current_letter_rank=re.sub(r"[+-]", '', mb.regression.letter_rank)
                )
            )

    def test_ranking_heuristic_on_code_with_a_change_and_regression_slow_down(self):
        """
        Will simulate a change on the dummy code that has a performance impact
        the heuristic should catch this change and give it a lower then acceptable letter rank.
        """
        test_definitions = [
            [{"slow_down": False}, {"slow_down": True}],  # Test 1
            [{"slow_down": False}, {"slow_down": True}],  # Test 2
            [{"slow_down": False}, {"slow_down": True}],  # Test 3
            [{"slow_down": False}, {"slow_down": True}],  # Test 4
        ]
        for tests in test_definitions:
            for instructions in tests:
                # Run a benchmark on our demo code.
                mb.test_case_name = "demo"
                mb.run(
                    method=FancyCode(instructions["slow_down"]).calculate_statistics_about_fancy_population,
                    arguments=[],
                    iteration=self.ITERATIONS,
                    pacing=0,
                )
            # Verify if the last letter rank fails to meet the predefined situation.
            self.assertFalse(
                check_letter_rank_boundary(
                    boundary_letter_rank="A",
                    current_letter_rank=re.sub(r"[+-]", '', mb.regression.letter_rank)
                )
            )

    def test_ranking_heuristic_on_code_with_a_change_and_no_regression(self):
        """
        Will force a change in the dummy code but the change has no performance
        impact therefore this test should not fail and result in a true.
        """
        test_definitions = [

            {"use_slow_method": False, "use_fast_method": False},  # Test 1
            {"use_slow_method": False, "use_fast_method": True}    # Test 2

        ]
        for instructions in test_definitions:
            # Run a benchmark on our demo code.
            mb.test_case_name = "demo"
            mb.run(
                method=FancyCode(
                    instructions["use_slow_method"],
                    instructions["use_fast_method"]
                ).calculate_statistics_about_fancy_population,
                arguments=[],
                iteration=self.ITERATIONS,
                pacing=0,
            )
            # Verify if the last letter rank fails to meet the predefined situation.
            self.assertTrue(
                check_letter_rank_boundary(
                    boundary_letter_rank="A",
                    current_letter_rank=re.sub(r"[+-]", '', mb.regression.letter_rank)
                )
            )

    def test_boundary_verification_max_and_min_thresholds(self):
        """
        This test will verify if the boundary mechanism is working correctly.
        It wil check the following things:

        - Does only max boundary check work?
        - Does only min boundary check work?
        - Does both a min & max boundary check work?

        """
        # Run a benchmark on our demo code.
        mb.test_case_name = "demo"
        mb.run(
            method=FancyCode().calculate_statistics_about_fancy_population,
            arguments=[],
            iteration=1,
            pacing=0,
        )
        # Verify if the boundary works with just the max boundary
        self.assertTrue(
            mb.verify_boundaries(
                boundaries=[
                    {
                        "name": "verify_max_recorded_latency",
                        "value": mb.benchmark_statistics.maximum_outlier,
                        "maximum": 10,
                        "minimum": None
                    }
                ]
            )
        )
        # Verify if the boundary works with just min boundary
        self.assertTrue(
            mb.verify_boundaries(
                boundaries=[
                    {
                        "name": "verify_max_recorded_latency",
                        "value": mb.benchmark_statistics.maximum_outlier,
                        "maximum": None,
                        "minimum": 0.000000000000000002
                    }
                ]
            )
        )
        # Verify both min and max boundary
        self.assertTrue(
            mb.verify_boundaries(
                boundaries=[
                    {
                        "name": "verify_max_recorded_latency",
                        "value": mb.benchmark_statistics.maximum_outlier,
                        "maximum": 10,
                        "minimum": 0.000000000000000002
                    }
                ]
            )
        )
