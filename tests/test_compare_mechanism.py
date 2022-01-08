from examples.non_intrusive_example_code import FancyCode
from QuickPotato import micro_benchmark as mb
from QuickPotato.statistical.verification import check_letter_rank_boundary
import unittest
import re


class TestHeuristics(unittest.TestCase):

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
        for _ in range(0, 10):
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
                    current_letter_rank=re.sub(r"[+-]", '', mb.distance_statistics.letter_rank)
                )
            )

    def test_ranking_heuristic_on_code_with_a_change_and_regression(self):
        """

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
                    current_letter_rank=re.sub(r"[+-]", '', mb.distance_statistics.letter_rank)
                )
            )
