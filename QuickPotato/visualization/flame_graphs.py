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
        self.count = 0
        # Properties of the stack trace
        self._collected_stack_trace = self.select_call_stack_by_sample_id(test_case_name, sample_id)
        self.discovered_root_frame = self._collected_stack_trace[0]['parent_function_name']
        self.x = self._discover_parent_child_relationships()
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

    def _recursively_count_children(self, dic, name):
        self.count += 1 if len(dic['children']) == 0 else len(dic['children'])
        for relationship in dic["children"]:
            self._recursively_count_children(relationship, name)

    def _discover_amount_of_relationships(self, dic):
        self._recursively_count_children(dic, dic["name"])
        dic['value'] = self.count
        print(f"{dic['name']} = {self.count}")
        self.count = 0
        for relationship in dic["children"]:
            self._discover_amount_of_relationships(relationship)
        return dic

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
        print(self._discover_amount_of_relationships(inheritance))
        return inheritance
