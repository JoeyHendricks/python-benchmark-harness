from .._database.collection import Crud
import numpy as np


class Statistics:

    def __init__(self, measurements):
        super(Statistics, self).__init__()

        self._collected_measurements = measurements

    @property
    def raw_data(self) -> list:
        """

        Returns
        -------

        """
        return self._collected_measurements

    @property
    def normalized_response_times(self) -> list:
        """

        Returns
        -------

        """
        measurements = np.array(self._collected_measurements)
        return measurements[abs(measurements - np.mean(measurements)) < 2 * np.std(measurements)]

    @property
    def average_response_time(self) -> float:
        """

        Returns
        -------

        """
        return float(sum(self._collected_measurements) / len(self._collected_measurements))

    @property
    def maximum_outlier(self) -> float:
        """

        Returns
        -------

        """
        return float(max(self._collected_measurements))

    @property
    def minimum_outlier(self) -> float:
        """

        Returns
        -------

        """
        return float(min(self._collected_measurements))

    @property
    def percentile_5th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 5))

    @property
    def percentile_10th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 10))

    @property
    def percentile_15th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 15))

    @property
    def percentile_20th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 20))

    @property
    def percentile_25th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 25))

    @property
    def percentile_30th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 30))

    @property
    def percentile_35th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 35))

    @property
    def percentile_40th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 40))

    @property
    def percentile_45th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 45))

    @property
    def percentile_50th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 50))

    @property
    def percentile_55th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 55))

    @property
    def percentile_60th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 60))

    @property
    def percentile_65th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 65))

    @property
    def percentile_70th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 70))

    @property
    def percentile_75th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 75))

    @property
    def percentile_80th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 80))

    @property
    def percentile_85th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 85))

    @property
    def percentile_90th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 90))

    @property
    def percentile_95th(self) -> float:
        """

        Returns
        -------

        """
        return float(np.percentile(np.array(self._collected_measurements), 95))


class CodePaths(Crud):

    def __init__(self):
        super().__init__()

        self._matched_code_path = None

    def _map_out_hierarchical_stack_relationships(self, url: str, tcn: str, sample_id: str) -> dict:
        """
        Will map out the parent child relationships for each function to form hierarchical data structure.
        This structure can than be used to generate D3 flame graphs.

        (Function uses recursion to travel through the hierarchical
        JSON stack until no more row in the collected stack trace can be found.)

        :param url: The _database connection url
        :param tcn: The test case name
        :param sample_id: The found sample id
        :return: An hierarchical data structure in JSON format.
        """
        stack = {}
        collected_stack = self.select_benchmark_call_stack_by_sample_id(url, tcn, sample_id)
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

    def _recursively_update_number_of_parent_child_relationship(self, stack: dict, parent: str, child: str) -> None:
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


