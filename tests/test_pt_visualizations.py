from QuickPotato.profiling.intrusive import performance_test as pt
from QuickPotato.statistical.visualizations import FlameGraph, CsvFile
from QuickPotato.configuration.management import options
from QuickPotato.utilities.defaults import default_test_case_name
from QuickPotato.database.queries import Crud
from examples.non_intrusive_example_code import fast_method
import unittest


class TestFlameGraphs(unittest.TestCase):

    def setUp(self):
        """

        """
        options.enable_intrusive_profiling = True
        # Making sure that the performance testing object is reset with -
        # new info and the quick profiling default test case.
        pt.test_case_name = default_test_case_name

    def tearDown(self):
        """

        """
        options.enable_intrusive_profiling = False
        self.clean_up()

    @staticmethod
    def clean_up():
        """

        """
        database_manager = Crud()
        database_manager.delete_result_database(default_test_case_name)

    def test_quick_profiling_flame_graphs(self):
        """

        :return:
        """
        fast_method()

        # Verify if HTML contain the following tags
        html = str(FlameGraph().html)
        self.assertIn("payload", html)
        self.assertIn("body", html)
        self.assertIn("html", html)
        self.assertIn("option", html)
