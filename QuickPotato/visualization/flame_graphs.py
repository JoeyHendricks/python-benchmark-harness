from QuickPotato.database.queries import Crud
import json
from QuickPotato.utilities.html_templates import html_template_svg_header, html_template_svg_frame


class FlameGraphGenerator(Crud):

    def __init__(self, test_case_name, sample_id, filter_noise=False):
        super(FlameGraphGenerator, self).__init__()

        # Properties of the stack trace
        self._collected_stack_trace = self.select_call_stack_by_sample_id(test_case_name, sample_id)
        self._root_frame = self._collected_stack_trace[0]['parent_function_name']
        self.filter_noise = filter_noise
        self._unmatched_calls = []

        with open('C:\\temp\\test.json', 'w') as file:
            json.dump(self.function_inheritance, file)

        exit()

    @property
    def function_inheritance(self):
        """

        :return:
        """
        return [line for line in self._discover_function_inheritance()]

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

    def _discover_function_inheritance(self):
        """

        :return:
        """
        inheritance_mapping = {}

        for line in self._collected_stack_trace:

            line = self._filter_out_noise(line)
            if line is None:
                # Row needs to be filtered
                pass

            elif line['parent_function_name'] == self._root_frame:
                inheritance_mapping[line['child_function_name']] = [self._root_frame]
                yield {
                        "name": line['child_function_name'],
                        "value": "",
                        "children": [self._root_frame]
                    }

            else:
                if line['parent_function_name'] in inheritance_mapping:

                    # Remove duplicates from history
                    frame = list(dict.fromkeys(inheritance_mapping[line['parent_function_name']]))

                    if frame[-1] != line['parent_function_name']:
                        frame.append(line['parent_function_name'])

                    inheritance_mapping[line['child_function_name']] = frame
                    yield {
                            "name": line['child_function_name'],
                            "value": "",
                            "children": frame
                        }

                else:
                    self._unmatched_calls.append(line)
