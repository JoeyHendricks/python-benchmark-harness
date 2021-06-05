from QuickPotato.database.queries import Crud
from QuickPotato.statistical.data import CodePaths
from QuickPotato.utilities.html_templates import flame_graph_template, heatmap_template
from QuickPotato.utilities.defaults import default_test_case_name
from QuickPotato.utilities.exceptions import UnableToGenerateVisualizations, \
    UnableToExportVisualization, UnAcceptableTestIdFound
from datetime import datetime
from jinja2 import Template
import plotly.graph_objects as go
import pandas as pd
import numpy
import json
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

        self.json = [
            self._count_code_path_length(self._map_out_hierarchical_stack_relationships(test_case_name, sample))
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
            name = f"FlameGraph-{self.test_case_name}-{datetime.now().timestamp()}"
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

    def __init__(self, test_case_name=default_test_case_name, test_ids=None, order_by="latency",
                 detect_code_paths=True):
        """

        :param test_case_name:
        :param test_ids:
        :param order_by:
        """
        super(HeatMap, self).__init__()
        self.list_of_test_ids = test_ids
        if test_ids is None and test_case_name == default_test_case_name:
            self.list_of_test_ids = [self.select_test_ids_with_performance_statistics(database=test_case_name)[-1]]

        elif test_ids is None or type(test_ids) is not list:
            raise UnableToGenerateVisualizations()

        self._decimals = 25
        self._order_by = order_by
        self.test_case_name = test_case_name
        self._all_recorded_method_response_times = []

        self.statistics = {}
        self.sample_list = {}
        for tid in test_ids:
            self.sample_list[tid] = self.select_all_sample_ids(test_case_name, tid)
            self.statistics[tid] = {}
            for sample in self.sample_list[tid]:
                self.statistics[tid][sample] = self.select_call_stack_by_sample_id(test_case_name, sample)

        self.json = self.generate_json_payload(detect_code_paths)

    def look_up_method_latency(self, parent_function_name, child_function_name, sample_id, test_id):
        """

        :param parent_function_name:
        :param child_function_name:
        :param sample_id:
        :param test_id:
        :return:
        """
        for frame in self.statistics[test_id][sample_id]:
            if frame["sample_id"] == sample_id and child_function_name == frame["child_function_name"] \
                    and parent_function_name == frame["parent_function_name"]:
                time = float(format(frame["cumulative_time"], f".{self._decimals}f").lstrip().rstrip('0'))
                return time

            else:
                continue

    def look_up_method_meta_data(self, parent_function_name, child_function_name, sample_id, test_id):
        """

        :param parent_function_name:
        :param child_function_name:
        :param sample_id:
        :param test_id:
        :return:
        """
        for frame in self.statistics[test_id][sample_id]:
            if frame["sample_id"] == sample_id and child_function_name == frame["child_function_name"] \
                    and parent_function_name == frame["parent_function_name"]:
                return {
                    "parent_path": frame["parent_path"],
                    "parent_line_number": frame["parent_line_number"],
                    "child_path": frame["child_path"],
                    "child_line_number": frame["child_line_number"],
                    "number_of_calls": frame["number_of_calls"],
                }

            else:
                continue

    @staticmethod
    def generate_y_axis_identifier(parent, child, sample_id):
        """
        
        :param parent: 
        :param child: 
        :param sample_id: 
        :return: 
        """
        if parent == sample_id:
            text = f"profiler/{child}".replace("<", " ")
            text = text.replace(">", "")
            return text
        else:
            text = f"{parent}/{child}".replace("<", " ")
            text = text.replace(">", " ")
            return text

    def generate_json_payload(self, detect_code_paths):
        """

        :return:
        """
        data = []
        for test_id in self.list_of_test_ids:

            if test_id == "None":
                raise UnAcceptableTestIdFound()

            for sample_id in self.sample_list[test_id]:

                if detect_code_paths:
                    hierarchical_stack = self._map_out_hierarchical_stack_relationships(self.test_case_name, sample_id)

                else:
                    hierarchical_stack = None

                for frame in self.statistics[test_id][sample_id]:

                    parent_function = frame['parent_function_name']
                    child_function = frame['child_function_name']

                    if hierarchical_stack is not None:
                        predicted_code_path = self._recursively_search_hierarchical_stack(
                            hierarchical_stack,
                            frame['parent_function_name'],
                            frame['child_function_name'],
                            history=[]
                        )
                    else:
                        predicted_code_path = "Code path could not be predicted."

                    meta_data = self.look_up_method_meta_data(
                        parent_function_name=frame['parent_function_name'],
                        child_function_name=frame['child_function_name'],
                        sample_id=sample_id,
                        test_id=test_id
                    )
                    latency = self.look_up_method_latency(
                        parent_function_name=frame['parent_function_name'],
                        child_function_name=frame['child_function_name'],
                        sample_id=sample_id,
                        test_id=test_id
                    )
                    data.append(
                        {
                            "y_axis_identifier_parent_child_pair": self.generate_y_axis_identifier(
                                parent_function,
                                child_function,
                                sample_id
                            ),
                            "x_axis_identifier_sample_ids": sample_id,
                            "x_axis_identifier_test_ids": test_id,
                            "predicted_code_path": predicted_code_path,
                            "meta_data": meta_data,
                            "latency": latency
                        }
                    )
                    self._all_recorded_method_response_times.append(latency)

        return json.dumps(sorted(data, key=lambda k: k[self._order_by], reverse=True))

    def render_html(self):
        """

        :return:
        """
        max_time = max(self._all_recorded_method_response_times)
        min_time = min(self._all_recorded_method_response_times)
        time_scale = list(numpy.logspace(numpy.log10(min_time), numpy.log10(max_time), num=4))
        template = Template(heatmap_template)
        return template.render(payload=self.json, time_scale=time_scale)

    def export(self, path):
        """
        Export the heatmap as a HTML report on disk.
        :param path: The path on disk where the file needs to be written.
                     Example: C:\\temp\\
        """
        if os.path.isdir(path):
            name = f"Heatmap-{self.test_case_name}-{datetime.now().timestamp()}"
            with open(f"{path}{name}.html", 'a') as file:
                file.write(self.render_html())
        else:
            raise UnableToExportVisualization()


class BarChart(Crud):

    def __init__(self, test_case_name=default_test_case_name, test_ids=None, order_by="latency"):
        """

        :param test_case_name:
        :param test_ids:
        :param order_by:
        """
        super(BarChart, self).__init__()

        # Sorting out the test-id's
        self.test_case_name = test_case_name
        self._order_by = order_by
        if test_ids is None or type(test_ids) is not list:
            raise UnableToGenerateVisualizations()

        elif test_ids is None and test_case_name == default_test_case_name:
            self.list_of_test_ids = [self.select_test_ids_with_performance_statistics(database=test_case_name)[-1]]

        else:
            self.list_of_test_ids = test_ids

        # Gathering relevant performance metrics
        self.statistics = {}
        for tid in self.list_of_test_ids:
            self.statistics[tid] = self.select_call_stack_by_test_id(test_case_name, tid)

        self.json = self.generate_json()

    def generate_json(self):
        """

        :return:
        """
        payload = []
        for tid in self.list_of_test_ids:
            for row in self.statistics[tid]:

                if row['parent_function_name'] == row['sample_id']:
                    method_signature = row['child_function_name']

                else:
                    method_signature = f"{row['parent_function_name']}/{row['child_function_name']}"

                payload.append(
                    {
                        "sample_id": row['sample_id'],
                        "test_id": tid,
                        "method_signature": method_signature,
                        "latency": row['cumulative_time']
                    }
                )
        return sorted(payload, key=lambda k: k[self._order_by], reverse=True)

    def render_html(self):
        """

        :return:
        """
        df = pd.DataFrame(self.json)
        fig = go.Figure()
        fig.update_layout(
            title="<span style='font-size: 22px;'>QuickPotato Method Performance Bar Chart</span>",
            template="ggplot2",
            xaxis=dict(title_text="Test-id's"),
            yaxis=dict(title_text="Time spent in seconds"),
            barmode="stack",
            font=dict(
                size=12,
            )
        )

        for method_signature in df.method_signature.unique():
            plot_df = df[df.method_signature == method_signature]
            fig.add_trace(
                go.Bar(
                    x=[plot_df.test_id, plot_df.sample_id],
                    y=plot_df.latency,
                    name=method_signature,
                    meta=[method_signature],
                    hovertemplate=
                    '<br>Test-ID: %{x[0]}</b>'
                    '<br>Sample-ID: %{x[1]}</b>'
                    '<br>method name: %{meta[0]}</b>' +
                    '<br>Time Spent %{y}</b>' +
                    '<extra></extra>'
                ),
            )

        return fig.to_html(config={
            "displaylogo": False
        })

    def export(self, path):
        """
        Export the bar chart as a HTML report on disk.
        :param path: The path on disk where the file needs to be written.
                     Example: C:\\temp\\
        """
        if os.path.isdir(path):
            name = f"BarChart-{self.test_case_name}-{datetime.now().timestamp()}"
            with open(f"{path}{name}.html", 'a') as file:
                file.write(self.render_html())
        else:
            raise UnableToExportVisualization()
