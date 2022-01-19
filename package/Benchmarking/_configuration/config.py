from os.path import isfile, dirname, realpath
import yaml
import sys


class Configuration(object):

    FILE_NAME = "options.yaml"
    DEFAULT_SETTINGS = {

        "enable_database_echo": False,
        "enable_asynchronous_payload_delivery": False,
        "enable_auto_clean_up_old_test_results": True,
        "maximum_number_saved_test_results": 100,

    }
    PATH = dirname(realpath(__file__)) + "\\" if "\\" in dirname(realpath(__file__)) else \
        dirname(realpath(__file__)) + "/"

    def __init__(self):
        """

        """
        if isfile(self.PATH + self.FILE_NAME) is False:
            self._dump_configuration_to_yaml_file(self.DEFAULT_SETTINGS)

        self.contents = yaml.safe_load(open(self.PATH + self.FILE_NAME))

    def _dump_configuration_to_yaml_file(self, contents: dict) -> None:
        """

        :param contents:
        :return:
        """
        with open(self.PATH + self.FILE_NAME, 'w') as file:
            yaml.dump(contents, file)

    @property
    def enable_database_echo(self) -> bool:
        """

        :return:
        """
        return self.contents["enable_database_echo"]

    @property
    def enable_asynchronous_payload_delivery(self) -> bool:
        return self.contents["enable_asynchronous_payload_delivery"]

    @property
    def enable_auto_clean_up_old_test_results(self) -> bool:
        """

        :return:
        """
        return self.contents["enable_auto_clean_up_old_test_results"]

    @property
    def set_max_saved_tests(self) -> int:
        """

        :return:
        """
        return self.contents["maximum_number_saved_test_results"]

    @enable_database_echo.setter
    def enable_database_echo(self, value: bool) -> None:
        """

        :param value:
        :return:
        """
        self.contents["enable_database_echo"] = value
        self._dump_configuration_to_yaml_file(self.contents)

    @enable_asynchronous_payload_delivery.setter
    def enable_asynchronous_payload_delivery(self, value: bool) -> None:
        """

        :param value:
        :return:
        """
        if sys.version_info[0:3] > (3, 8, 2) and value is True:
            self.contents["enable_asynchronous_payload_delivery"] = True
            self._dump_configuration_to_yaml_file(self.contents)

        else:
            self.contents["enable_asynchronous_payload_delivery"] = False
            self._dump_configuration_to_yaml_file(self.contents)

    @enable_auto_clean_up_old_test_results.setter
    def enable_auto_clean_up_old_test_results(self, value: bool) -> None:
        """

        :param value:
        :return:
        """
        self.contents["enable_auto_clean_up_old_test_results"] = value
        self._dump_configuration_to_yaml_file(self.contents)

    @set_max_saved_tests.setter
    def set_max_saved_tests(self, value: bool) -> None:
        """

        :param value:
        :return:
        """
        self.contents["maximum_number_saved_test_results"] = value
        self._dump_configuration_to_yaml_file(self.contents)
