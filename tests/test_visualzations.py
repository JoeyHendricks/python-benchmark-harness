from tests.stubs import FancyCode
from package.Benchmarking import benchmark as mb
from package.Benchmarking.visualizations.flame_graphs import FlameGraph
import unittest


class TestVerifications(unittest.TestCase):

    ITERATIONS = 10

    def _create_basic_baseline_in_unit_test_database(self):
        """
        Will create an stable baseline run in the database.
        """
        mb.test_case_name = "unit_test"
        mb.run(
            method=FancyCode().calculate_statistics_about_fancy_population,
            arguments=[],
            iteration=self.ITERATIONS,
            pacing=0,
        )
        return {"baseline_test_id": mb.baseline_test_id, "benchmark_test_id": mb.test_id}

    def test_flame_graph_html_rendering(self):
        """
        Will verify if the HTML is for the flame graphs is rendered correctly.
        This done by checking that a number of key values are there in the
        raw html export.
        """
        test_ids = self._create_basic_baseline_in_unit_test_database()
        graph = FlameGraph(
            test_case_name="unit_test",
            database_connection_url=mb.database_connection_url,
            test_id=test_ids["benchmark_test_id"]
        )
        # check if rendering is correct
        self.assertTrue(True if "calculate_statistics_about_fancy_population" in graph.html else False)
        self.assertTrue(True if "flameGraph" in graph.html else False)
        self.assertTrue(True if "d3.flamegraph()" in graph.html else False)
