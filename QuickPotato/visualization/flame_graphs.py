from QuickPotato.database.queries import Crud


class HierarchicalFoldedStack(Crud):

    def __init__(self, test_case_name, sample_id):
        super(HierarchicalFoldedStack, self).__init__()

        self.collected_stack_trace = self.select_call_stack_by_sample_id(test_case_name, sample_id)
        self.discovered_root_frame = self.collected_stack_trace[0]['parent_function_name']
        self._current_number_of_children = 0

    @property
    def json(self):
        """
        When accessed it wil generate a JSON data structure
        suitable for rendering D3 flame graphs.

        :return: An hierarchical data structure in JSON format.
        """
        return self._discover_relationships()

    def _recursively_update_parent_child_relationship(self, stack, parent, child):
        """
        Helps map out the call stack by extending or updating the
        hierarchical stack with new members.
        (Function is recursive until there are no more objects in the stack.)

        :param stack: The hierarchical JSON call stack.
        :param parent: The name of the parent function.
        :param child: The name of the child function.
        """
        if stack['name'] == parent:
            stack['children'].append(
                {
                    "name": child,
                    "children": []
                }
            )

        else:
            for item in stack['children']:
                self._recursively_update_parent_child_relationship(item, parent, child)

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

    def _count_relationships(self, stack):
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
            self._count_relationships(relationship)
        return stack

    def _discover_relationships(self):
        """
        Will map out the parent child relationships for each function to form hierarchical data structure.
        This structure can than be used to generate D3 flame graphs.
        (Function uses recursion to travel through the hierarchical
        JSON stack until no more row in the collected stack trace can be found.)

        :return: An hierarchical data structure in JSON format.
        """
        stack = {}
        for line in self.collected_stack_trace:

            if line["parent_function_name"] == self.discovered_root_frame:
                stack["name"] = line["parent_function_name"]
                stack["children"] = [
                    {
                        "name": line["child_function_name"],
                        "children": []
                    }
                ]

            else:
                self._recursively_update_parent_child_relationship(
                    stack=stack,
                    parent=line['parent_function_name'],
                    child=line['child_function_name']
                )
        return self._count_relationships(stack)
