from .._utilities.exceptions import UnableToGenerateVisualizations, UnableToExportVisualization
from .._templates.flame_graph import flame_graph_template
from ..statistical.measurements import CodePaths
from datetime import datetime
from jinja2 import Template
import os


class FlameGraph(CodePaths):

    def __init__(self, test_case_name: str, database_connection_url: str, test_id=None) -> None:
        """

        When initialized it will generate a hieratical json stack for each sample
        in the test id attached to the specified test case and make it possible to render D3-flame-graphs.
        For more info about D3-flame-graphs visit:

        https://github.com/spiermar/d3-flame-graph

        :param test_case_name: The name of the test case (This is also always the _database name).
                               If test case name is not defined it will default to the quick profiling
                               _database/test case name.
        :param test_id: The generated test id, if it is not defined and the test case is rolled to
                        default the latest available test id wil be used.
        :param database_connection_url: The connection url to the _database.
        """
        super(FlameGraph, self).__init__()
        if test_id is None:
            raise UnableToGenerateVisualizations()

        self.list_of_samples = self.select_all_sample_ids_in_benchmark_by_test_id(
            url=database_connection_url,
            tcn=test_case_name,
            test_id=test_id
        )
        self._current_number_of_children = 0
        self.test_case_name = test_case_name
        self.json = [
            self._count_code_path_length(
                self._map_out_hierarchical_stack_relationships(
                    url=database_connection_url,
                    tcn=test_case_name,
                    sample_id=sample_id
                )
            )
            for sample_id in self.list_of_samples
        ]
        self.html = self._render_html()

    def export(self, path: str) -> None:
        """
        Export the flame graph as a HTML report on disk.
        :param path: The path on disk where the file needs to be written.
                     Example: C:\\temp\\
        """
        if os.path.isdir(path):
            name = f"FlameGraph-{self.test_case_name}-{datetime.now().timestamp()}"
            with open(f"{path}{name}.html", 'a') as file:
                file.write(self.html)
        else:
            raise UnableToExportVisualization()

    def _render_html(self) -> Template.render:
        """
        Renders a HTML web page that contains the flame graph.
        :return: A filled in HTML template
        """
        template = Template(flame_graph_template)
        return template.render(
            list_of_samples=self.list_of_samples,
            payload=self.json,
        )

    def _recursively_count_samples(self, stack: dict, function_name: str) -> None:
        """
        Will count how many children/samples the given function name has.

        (Function is recursive and will travel through the hierarchical
        JSON stack until no more member can be found.)

        :param stack: The discovered hierarchical JSON call stack without the amount of samples.
        :param function_name: The name of the member function
        """
        self._current_number_of_children += 1 if len(stack['children']) == 0 else len(stack['children'])
        for relationship in stack["children"]:
            self._recursively_count_samples(relationship, function_name)

    def _count_code_path_length(self, stack: dict) -> dict:
        """
        Will travel down the discovered hierarchical stack and add the amount of samples per member.

        (Function is recursive and will travel through the hierarchical
        JSON stack until no more member can be found.)

        :param stack: The discovered hierarchical JSON call stack without the amount of samples.
        :return: The discovered hierarchical JSON call with the amount of samples per member.
        """
        self._recursively_count_samples(stack, stack["name"])
        stack['value'] = self._current_number_of_children
        self._current_number_of_children = 0
        for relationship in stack["children"]:
            self._count_code_path_length(relationship)
        return stack
