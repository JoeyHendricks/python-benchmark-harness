from QuickPotato.database.queries import Crud
from QuickPotato.utilities.html_templates import html_template_svg_header, html_template_svg_frame
from random import choice
from string import ascii_uppercase, digits
from jinja2 import Template
import pandas as pd
import sys


class FlameGraphGenerator(Crud):

    def __init__(self, test_case_name, sample_id, filter_noise=False):
        super(FlameGraphGenerator, self).__init__()

        # Properties of the stack trace
        self._collected_stack_trace = self.select_call_stack_by_sample_id(test_case_name, sample_id)
        self.discovered_root_frame = self._collected_stack_trace[0]['parent_function_name']

        # Filters
        self.filter_noise = filter_noise

        # Information collected and the mappings made out of the stack trace.
        self._unmatched_calls = []
        self._mapping = []
        self._cumulative_time = []
        self._walk_through_stack()
        self._max_observed_time = max(self._cumulative_time)
        self._min_observed_time = min(self._cumulative_time)
        self.folded_stack, self.meta_data = self._generate_folded_stack()

        # Flame Graph Options
        self.colors = [(255, 236, 25), (255, 152, 0), (246, 65, 45)]  # Yellow - Orange - Red
        self.width = 930
        self.height = (self.folded_stack.shape[1] * 25) + 100
        self._flame_graph = self._build_svg_flame_graph()

    def _filter_out_noise(self, row):
        """

        :param row:
        :return:
        """
        if self.filter_noise and "site-packages" in row["child_path"] or "Program Files" in row["child_path"]:
            return None

        elif self.filter_noise and "importlib" in row["child_path"] or "<string>" in row["child_path"]:
            return None

        elif self.filter_noise and "~" in row["child_path"]:
            return None

        else:
            return row

    def _collect_inheritance_information(self, row, function_inheritance):
        """

        :param row:
        :param function_inheritance:
        :return:
        """
        self._cumulative_time.append(row["cumulative_time"])
        row = self._filter_out_noise(row)
        if row is None:
            # Row needs to be filtered
            pass

        elif row['parent_function_name'] == self.discovered_root_frame:
            function_inheritance[row['child_function_name']] = [self.discovered_root_frame]
            self._mapping.append(
                {
                    "child_function_name": row['child_function_name'],
                    "parent_function_name": row['parent_function_name'],
                    "inheritance": [self.discovered_root_frame],
                    "path": row['child_path'],
                    "line_number": row['child_line_number'],
                    "number_of_calls": row['number_of_calls'],
                    "total_time": row['total_time'],
                    "cumulative_time": row['cumulative_time'],
                }
            )

        else:
            if row['parent_function_name'] in function_inheritance:

                # Remove duplicates from history
                frame = list(dict.fromkeys(function_inheritance[row['parent_function_name']]))

                if frame[-1] != row['parent_function_name']:
                    frame.append(row['parent_function_name'])

                function_inheritance[row['child_function_name']] = frame
                self._mapping.append(
                    {
                        "child_function_name": row['child_function_name'],
                        "parent_function_name": row['parent_function_name'],
                        "inheritance": frame,
                        "path": row['child_path'],
                        "line_number": row['child_line_number'],
                        "number_of_calls": row['number_of_calls'],
                        "total_time": row['total_time'],
                        "cumulative_time": row['cumulative_time'],
                    }
                )

            else:
                self._unmatched_calls.append(row)
