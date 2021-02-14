from QuickPotato.database.queries import Crud
from QuickPotato.utilities.html_templates import html_template_svg_header, html_template_svg_frame
from random import choice
from string import ascii_uppercase, digits
from jinja2 import Template
import pandas as pd
import sys
import collections


class FlameGraphGenerator(Crud):

    def __init__(self, test_case_name, sample_id, filter_noise=False):
        super(FlameGraphGenerator, self).__init__()

        # Properties of the stack trace
        self._collected_stack_trace = self.select_call_stack_by_sample_id(test_case_name, sample_id)
        self.discovered_root_frame = self._collected_stack_trace[0]['parent_function_name']
        self._discover_parent_child_relationships()
        exit()

    def _recursively_update_parent_child_relationship(self, dic, parent, child):

        if dic['name'] == parent:
            dic['children'].append(
                {
                    "name": child,
                    "children": []
                }
            )

        else:
            for item in dic['children']:
                self._recursively_update_parent_child_relationship(item, parent, child)  # <-- recursion

    def _recursively_count_relationships(self, dic):
        print(dic['name'])
        dic['value'] = 1 if len(dic["children"]) == 0 else len(dic["children"])
        print(dic['value'])
        print(len(dic['children']))
        print(dic['children'])
        exit()
        for item in dic['children']:
            self._recursively_count_relationships(item)  # <-- recursion

    def _discover_parent_child_relationships(self):
        """

            :return:
            """

        inheritance = {}
        for line in self._collected_stack_trace:

            if line["parent_function_name"] == self.discovered_root_frame:
                inheritance["name"] = line["parent_function_name"]
                inheritance["children"] = [
                    {
                        "name": line["child_function_name"],
                        "children": []
                    }
                ]

            else:
                self._recursively_update_parent_child_relationship(
                    dic=inheritance,
                    parent=line['parent_function_name'],
                    child=line['child_function_name']
                )
        self._recursively_count_relationships(inheritance)
        print(inheritance)
        return inheritance
