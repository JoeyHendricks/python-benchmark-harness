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
        self.filter_external_libraries = filter_noise
        self.filter_builtin = filter_noise

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

    @property
    def svg_flame_graph(self):
        """

        :return:
        """
        return self._flame_graph

    def _pick_frame_color(self, value):
        if self._min_observed_time == self._max_observed_time and self._max_observed_time == value:
            return 246, 65, 45
        i_f = float(value - self._min_observed_time) / float(self._max_observed_time -
                                                             self._min_observed_time) * (len(self.colors) - 1)
        i, f = int(i_f // 1), i_f % 1
        if f < sys.float_info.epsilon:
            return self.colors[i]
        else:
            (r1, g1, b1), (r2, g2, b2) = self.colors[i], self.colors[i + 1]
            return int(r1 + f * (r2 - r1)), int(g1 + f * (g2 - g1)), int(b1 + f * (b2 - b1))

    def _collect_inheritance_information(self, row, function_inheritance):

        self._cumulative_time.append(row["cumulative_time"])
        if self.filter_external_libraries and "site-packages" in row["child_path"]:
            # Do not add call to mapping
            pass

        elif self.filter_builtin and "~" in row["child_path"]:
            # Do not add call to mapping
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

    def _walk_through_stack(self):
        """

        """
        function_inheritance = {}

        for row in self._collected_stack_trace:
            self._collect_inheritance_information(row, function_inheritance)

        count = 0  # <-- Keeping track of number of iteration to prevent infinite loop

        while len(self._unmatched_calls) == 0:

            if count > 5:
                break  # <-- exit strategy ;)

            count += 1
            for row in self._unmatched_calls:
                try:
                    self._collect_inheritance_information(row, function_inheritance)

                except KeyError:
                    self._unmatched_calls.append(row)

    def _generate_folded_stack(self):
        """

        :return:
        """
        inheritance_mapping = pd.DataFrame(self._mapping).sort_values(by=['parent_function_name'], ascending=False)
        folded_stack = []
        meta_data = {
            self._collected_stack_trace[0]['parent_function_name']: [
                self._collected_stack_trace[0]['parent_path'],
                self._collected_stack_trace[0]['parent_line_number'],
                self._collected_stack_trace[0]['number_of_calls'],
                self._collected_stack_trace[0]['total_time'],
                self._collected_stack_trace[0]['cumulative_time'],
            ]
        }

        # unpacking call stack information
        for row in inheritance_mapping.values:
            frame = list(dict.fromkeys(row[2] + [row[0]]))
            folded_stack.append(frame)
            meta_data[row[0]] = [row[3], row[4], row[5], row[6], row[7]]

        # Order folded stack alphabetically.
        folded_stack = pd.DataFrame(folded_stack)
        folded_stack = folded_stack.sort_values(by=[n for n in range(1, int(folded_stack.shape[1] / 2) + 1)])
        return folded_stack, meta_data

    def _generate_build_instructions(self):
        """

        :return:
        """
        current_y_position = self.height

        for depth, frame in enumerate(self.folded_stack.transpose().values):

            width = self.width / len(frame)
            current_x_position = 0
            previous_function_name = None
            previous_function_id = None
            all_coordinates_of_row = {}

            for function in frame:

                if function is None:
                    current_x_position += width

                elif previous_function_name == function:
                    previous_function_name = function

                    current_x_position += width
                    all_coordinates_of_row[previous_function_id]["width"] += width

                else:
                    previous_function_name = function
                    previous_function_id = ''.join(choice(ascii_uppercase + digits) for _ in range(12))

                    meta_data = self.meta_data[function]
                    all_coordinates_of_row[previous_function_id] = {
                        "function_name": function.strip("<>"),
                        "y_position": current_y_position,
                        "x_position": current_x_position,
                        "width": width,
                        "path": meta_data[0].strip("<>"),
                        "line_number": meta_data[1],
                        "number_of_calls": meta_data[2],
                        "total_time": meta_data[3],
                        "cumulative_time": meta_data[4],
                    }
                    current_x_position += width

            current_y_position -= 25
            for key in all_coordinates_of_row:
                yield all_coordinates_of_row[key]

    def _build_svg_flame_graph(self):
        """

        :return:
        """
        svg_image = html_template_svg_header.format(self.width, self.height, self.width, self.height + 25)
        for frame in self._generate_build_instructions():
            frame["color"] = self._pick_frame_color(frame['cumulative_time'])
            svg_image += html_template_svg_frame.format(**frame)
        svg_image += "\n</svg>"
        return svg_image
