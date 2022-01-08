from examples.non_intrusive_example_code import FancyCode
from QuickPotato import micro_benchmark as mb
#from QuickPotato._utilities.helpers import block_print_to_console, enable_print_to_console
from QuickPotato.visualizations._line_graphs import LineGraph
import unittest


class TestPerformance(unittest.TestCase):

    def test_ranking_mechanism_on_live_code(self):
        """

        """
        ranks = []
        ks_values = []
        ws_values = []

        for _ in range(0, 10):
            mb.test_case_name = "demo"
            mb.run(
                method=FancyCode().say_my_name_and_more,
                arguments=["Joey"],
                iteration=2,
                pacing=0,
                processes=10
            )
            mb.compare_benchmark(
                minimum_score=90,
                minimum_letter_rank="A"
            )
            ks_values.append(mb.distance_statistics.kolmogorov_smirnov_distance)
            ws_values.append(mb.distance_statistics.wasserstein_distance)
            ranks.append(mb.distance_statistics.rank)
            LineGraph(
                benchmark=mb.distance_statistics.sample_a,
                baseline=mb.distance_statistics.sample_b,
                kolmogorov_smirnov_distance=mb.distance_statistics.kolmogorov_smirnov_distance,
                wasserstein_distance=mb.distance_statistics.wasserstein_distance,
                rank=mb.rank,
                score=mb.score,
                change=0
            ).show()

        print(ks_values)
        print(ws_values)
        print(ranks)

