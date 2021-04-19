from QuickPotato.database.queries import Crud
from QuickPotato.statistical.data import CodePaths
from QuickPotato.utilities.html_templates import flame_graph_template
from QuickPotato.utilities.defaults import default_test_case_name
from QuickPotato.utilities.exceptions import UnableToGenerateVisualizations, UnableToExportVisualization
from datetime import datetime
from jinja2 import Template
import pandas as pd
import json
import re
import os


class FlameGraph(CodePaths):

    def __init__(self, test_case_name=default_test_case_name, test_id=None):
        """
        When initialized it will generate a hieratical json stack for each sample
        in the test id attached to the specified test case and make it possible to render D3-flame-graphs.
        For more info about D3-flame-graphs visit:

        https://github.com/spiermar/d3-flame-graph

        :param test_case_name: The name of the test case (This is also always the database name).
                               If test case name is not defined it will default to the quick profiling
                               database/test case name.
        :param test_id: The generated test id, if it is not defined and the test case is rolled to
                        default the latest available test id wil be used.
        """
        super(FlameGraph, self).__init__()

        if test_id is None and test_case_name == default_test_case_name:
            test_id = self.select_test_ids_with_performance_statistics(database=test_case_name)[-1]

        elif test_id is None:
            raise UnableToGenerateVisualizations()

        self.list_of_samples = self.select_all_sample_ids(test_case_name, test_id)
        self._current_number_of_children = 0
        self.test_case_name = test_case_name

        self.json = [self._count_code_path_length(self._map_out_hierarchical_stack_relationships(test_case_name, sample))
                     for sample in self.list_of_samples
                     ]
        self.html = self._render_html()

    def export(self, path):
        """
        Export the flame graph as a HTML report on disk.
        :param path: The path on disk where the file needs to be written.
                     Example: C:\\temp\\
        """
        if os.path.isdir(path):
            name = f"{self.test_case_name}-{datetime.now().timestamp()}"
            with open(f"{path}{name}.html", 'a') as file:
                file.write(self.html)
        else:
            raise UnableToExportVisualization()

    def _render_html(self):
        """
        Renders a HTML web page that contains the flame graph.
        :return: A filled in HTML template
        """
        template = Template(flame_graph_template)
        return template.render(
            list_of_samples=self.list_of_samples,
            payload=self.json,
        )

    def _recursively_count_samples(self, stack, function_name):
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

    def _count_code_path_length(self, stack):
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


class CsvFile(Crud):

    def __init__(self, test_case_name=default_test_case_name, test_id=None, delimiter=","):
        """
        Will build up the object, when no test id is given and when test case name is default.
        It will take the last known test id.

        :param test_case_name: The name of the test case
        :param delimiter: The delimiter of the csv file
        :param test_id: The test id within the test case
        """
        super(CsvFile, self).__init__()
        self.test_case_name = test_case_name
        self.delimiter = delimiter
        self.test_id = test_id

        if self.test_id is None and test_case_name == default_test_case_name:
            self.test_id = self.select_test_ids_with_performance_statistics(database=test_case_name)[-1]

        elif self.test_id is None:
            raise UnableToGenerateVisualizations()

        self.list_of_samples = self.select_all_sample_ids(test_case_name, self.test_id)

    def export(self, path):
        """
        Will export the csv file to a directory on the disk.
        :param path: The path on disk where the file needs to be written.
                     Example: C:\\temp\\
        """
        if os.path.isdir(path):
            content = []
            for sample_id in self.list_of_samples:
                stack = self.select_call_stack_by_sample_id(self.test_case_name, sample_id)
                for line in stack:
                    content.append(line)

            pd.DataFrame(content).to_csv(
                path_or_buf=f"{path}raw_export_of_{self.test_id}_{str(datetime.now().timestamp())}.csv",
                sep=self.delimiter,
                index=False
            )

        else:
            raise UnableToExportVisualization()


class HeatMap(CodePaths):

    def __init__(self, test_case_name=default_test_case_name, test_id=None):
        """

        :param test_case_name:
        :param test_id:
        """
        super(HeatMap, self).__init__()

        if test_id is None and test_case_name == default_test_case_name:
            test_id = self.select_test_ids_with_performance_statistics(database=test_case_name)[-1]

        elif test_id is None:
            raise UnableToGenerateVisualizations()

        self.response_times = []
        self._decimals = 25
        self.list_of_samples = self.select_all_sample_ids(test_case_name, test_id)
        self.test_case_name = test_case_name
        self._timings = self.select_unique_timings_per_function(test_case_name, test_id)

    def look_up_method_time(self, name, sample_id):
        """

        :param name:
        :param sample_id:
        :return:
        """
        for function in self._timings:
            if function["sample_id"] == sample_id and name == function["function_name"]:
                time = float(format(function["time"], f".{self._decimals}f").lstrip().rstrip('0'))
                self.response_times.append(time)
                return time

            else:
                continue

    @staticmethod
    def generate_tool_tip_message(stack, time):
        """

        :param stack:
        :param time:
        :return:
        """
        parent = re.sub(r'[^\w\d]', ' ', str(stack[-2]))
        function = re.sub(r'[^\w\d]', ' ', str(stack[-1]))
        return f"{parent}/{function} ran for: {time} .Sec"

    @staticmethod
    def convert_code_path_to_unique_string(stack):
        """

        :param stack:
        :return:
        """
        del stack[0]
        text = "/"
        for function in stack:
            text = text + re.sub(r'[^\w]', ' ', str(function))
            text.strip()
        return text

    @property
    def code_paths(self):
        """

        :return:
        """
        unique_code_paths = []
        for sample in self.list_of_samples:
            hierarchical_stack = self._map_out_hierarchical_stack_relationships(self.test_case_name, sample)
            for path in self._discover_code_paths(hierarchical_stack):
                function = path[-1]
                time_spent = self.look_up_method_time(function, sample)
                unique_code_paths.append(
                    {
                        "tooltip": self.generate_tool_tip_message(path, time_spent),
                        "sample_id": sample,
                        "path": self.convert_code_path_to_unique_string(path),
                        "history": path,
                        "time": time_spent,
                    }
                )
        return json.dumps(sorted(unique_code_paths, key=lambda k: k['time'], reverse=True))


