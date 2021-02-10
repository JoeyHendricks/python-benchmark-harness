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
        self._unmatched_calls = []
        self.d3_json()
        exit()

    def _collect_inheritance_information(self):
        """

        :return:
        """
        function_inheritance = {}
        for row in self._collected_stack_trace:
            if row is None:
                # Row needs to be filtered
                pass

            elif row['parent_function_name'] == self.discovered_root_frame:
                function_inheritance[row['child_function_name']] = [self.discovered_root_frame]

            else:
                if row['parent_function_name'] in function_inheritance:

                    # Remove duplicates from history
                    frame = list(dict.fromkeys(function_inheritance[row['parent_function_name']]))

                    if frame[-1] != row['parent_function_name']:
                        frame.append(row['parent_function_name'])

                    function_inheritance[row['child_function_name']] = frame

                else:
                    self._unmatched_calls.append(row)

        return function_inheritance

    def d3_json(self):

        inheritance = self._collect_inheritance_information()
        print("--------------------------------------------")
        for i in inheritance:
            print(f"child: {i} parents: {inheritance[i]}")

