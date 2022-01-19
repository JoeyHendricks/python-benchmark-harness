from .._utilities.exceptions import UnableToGenerateVisualizations, UnableToExportVisualization, UnAcceptableTestIdFound
from ..statistical.measurements import CodePaths
from .._templates.heatmap import heatmap_template
from datetime import datetime
from jinja2 import Template
import numpy
import json
import os


class HeatMap(CodePaths):

    def __init__(self, test_case_name: str, database_connection_url: str,
                 test_ids=None, order_by="latency", detect_code_paths=True) -> None:
        """

        :param test_case_name:
        :param database_connection_url
        :param test_ids:
        :param order_by:
        """
        super(HeatMap, self).__init__()
        self.list_of_test_ids = test_ids
        if test_ids is None or type(test_ids) is not list:
            raise UnableToGenerateVisualizations()

        self._decimals = 25
        self._order_by = order_by
        self.test_case_name = test_case_name
        self.database_connection_url = database_connection_url
        self._all_recorded_method_response_times = []

        self.statistics = {}
        self.sample_list = {}
        for tid in test_ids:
            self.sample_list[tid] = self.select_all_sample_ids_in_benchmark_by_test_id(
                url=database_connection_url,
                tcn=test_case_name,
                test_id=tid
            )
            self.statistics[tid] = {}
            for sample in self.sample_list[tid]:
                self.statistics[tid][sample] = self.select_benchmark_call_stack_by_sample_id(
                    url=database_connection_url,
                    tcn=test_case_name,
                    sample_id=sample
                )

        self.json = self.generate_json_payload(detect_code_paths)

    def look_up_method_latency(self, parent_func_name: str, child_func_name: str, sample_id: str, test_id) -> float:
        """

        :param parent_func_name:
        :param child_func_name:
        :param sample_id:
        :param test_id:
        :return:
        """
        for frame in self.statistics[test_id][sample_id]:
            if frame["sample_id"] == sample_id and child_func_name == frame["child_function_name"] \
                    and parent_func_name == frame["parent_function_name"]:
                time = float(format(frame["cumulative_time"], f".{self._decimals}f").lstrip().rstrip('0'))
                return time

            else:
                continue

    def find_method_meta_data(self, parent_func_name: str, child_func_name: str, sample_id: str, test_id: str) -> dict:
        """

        :param parent_func_name:
        :param child_func_name:
        :param sample_id:
        :param test_id:
        :return:
        """
        for frame in self.statistics[test_id][sample_id]:
            if frame["sample_id"] == sample_id and child_func_name == frame["child_function_name"] \
                    and parent_func_name == frame["parent_function_name"]:
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
    def generate_y_axis_identifier(parent: str, child: str, sample_id: str) -> str:
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

    def generate_json_payload(self, detect_code_paths: bool) -> json.dumps:
        """

        :return:
        """
        data = []
        for test_id in self.list_of_test_ids:

            if test_id == "None":
                raise UnAcceptableTestIdFound()

            for sample_id in self.sample_list[test_id]:

                if detect_code_paths:
                    hierarchical_stack = self._map_out_hierarchical_stack_relationships(
                        url=self.database_connection_url,
                        tcn=self.test_case_name,
                        sample_id=sample_id
                    )

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

                    meta_data = self.find_method_meta_data(
                        parent_func_name=frame['parent_function_name'],
                        child_func_name=frame['child_function_name'],
                        sample_id=sample_id,
                        test_id=test_id
                    )
                    latency = self.look_up_method_latency(
                        parent_func_name=frame['parent_function_name'],
                        child_func_name=frame['child_function_name'],
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

    def render_html(self) -> Template.render:
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
