from QuickPotato.database.queries import Crud
import numpy as np


class RawData(Crud):

    def __init__(self, test_id, database_name):
        super(RawData, self).__init__()

        self.test_id = test_id
        self.database_name = database_name
        self._response_times = self.select_response_times(self.database_name, self.test_id)

    def response_times(self):
        """

        Returns
        -------

        """
        return self._response_times

    def normalized_response_times(self):
        """

        Returns
        -------

        """
        measurements = np.array(self._response_times)
        return measurements[abs(measurements - np.mean(measurements)) < 2 * np.std(measurements)]

    def average_response_time(self):
        """

        Returns
        -------

        """
        return sum(self._response_times) / len(self._response_times)

    def maximum_outlier_in_response_times(self):
        """

        Returns
        -------

        """
        return max(self._response_times)

    def minimum_outlier_in_response_times(self):
        """

        Returns
        -------

        """
        return min(self._response_times)

    def percentile_5th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 5)

    def percentile_10th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 10)

    def percentile_15th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 15)

    def percentile_20th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 20)

    def percentile_25th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 25)

    def percentile_30th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 30)

    def percentile_35th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 35)

    def percentile_40th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 40)

    def percentile_45th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 45)

    def percentile_50th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 50)

    def percentile_55th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 55)

    def percentile_60th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 60)

    def percentile_65th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 65)

    def percentile_70th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 70)

    def percentile_75th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 75)

    def percentile_80th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 80)

    def percentile_85th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 85)

    def percentile_90th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 90)

    def percentile_95th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 95)


class CodePaths(Crud):

    def __init__(self):
        super().__init__()

        self._matched_code_path = None

    def _map_out_hierarchical_stack_relationships(self, test_case_name, sample_id):
        """
        Will map out the parent child relationships for each function to form hierarchical data structure.
        This structure can than be used to generate D3 flame graphs.

        (Function uses recursion to travel through the hierarchical
        JSON stack until no more row in the collected stack trace can be found.)

        :return: An hierarchical data structure in JSON format.
        """
        stack = {}
        collected_stack = self.select_call_stack_by_sample_id(test_case_name, sample_id)
        for line in collected_stack:

            if line["parent_function_name"] == collected_stack[0]['parent_function_name']:
                stack["name"] = line["parent_function_name"]
                stack["children"] = [
                    {
                        "name": line["child_function_name"],
                        "children": []
                    }
                ]

            else:
                self._recursively_update_number_of_parent_child_relationship(
                    stack=stack,
                    parent=line['parent_function_name'],
                    child=line['child_function_name']
                )
        return stack

    def _recursively_update_number_of_parent_child_relationship(self, stack, parent, child):
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
                self._recursively_update_number_of_parent_child_relationship(item, parent, child)

    def _recursively_search_hierarchical_stack(self, hierarchical_stack, parent, child, history):
        """

        :param hierarchical_stack:
        :param parent:
        :return:
        """
        if len(hierarchical_stack["children"]) != 0 and hierarchical_stack["name"] not in history:
            history.append(hierarchical_stack["name"])
        if hierarchical_stack["name"] == parent:
            matched_code_path = history
            matched_code_path.append(child)
            return matched_code_path

        else:
            for current_point_in_stack in hierarchical_stack["children"]:
                match = self._recursively_search_hierarchical_stack(
                    current_point_in_stack,
                    parent,
                    child,
                    history
                )
                if match is not None:
                    return match

                else:
                    continue


