from QuickPotato.utilities.defaults import default_quick_potato_configuration
from os.path import isfile, dirname, realpath
import yaml
import sys


class Configuration(object):

    FILE_NAME = "options.yaml"
    PATH = dirname(realpath(__file__)) + "\\" if "\\" in dirname(realpath(__file__)) else \
        dirname(realpath(__file__)) + "/"

    def __init__(self):

        if isfile(self.PATH + self.FILE_NAME) is False:
            self.dump_configuration_to_yaml_file(default_quick_potato_configuration)

        self.contents = yaml.safe_load(open(self.PATH + self.FILE_NAME))

    def dump_configuration_to_yaml_file(self, contents):
        with open(self.PATH + self.FILE_NAME, 'w') as file:
            yaml.dump(contents, file)

    @property
    def enable_intrusive_profiling(self):
        return self.contents["enable_intrusive_profiling"]

    @enable_intrusive_profiling.setter
    def enable_intrusive_profiling(self, value):
        self.contents["enable_intrusive_profiling"] = value
        self.dump_configuration_to_yaml_file(self.contents)

    @property
    def enable_policy_to_filter_out_invalid_test_ids(self):
        return self.contents["enable_the_selection_of_untested_or_failed_test_ids"]

    @enable_policy_to_filter_out_invalid_test_ids.setter
    def enable_policy_to_filter_out_invalid_test_ids(self, value):
        self.contents["enable_the_selection_of_untested_or_failed_test_ids"] = value
        self.dump_configuration_to_yaml_file(self.contents)

    @property
    def connection_url(self):
        """Specify which database vendor you want to use.
        For SQLite: "sqlite:///C:\\temp\\"
        For MySQL:  "mysql+pymysql://user:password@localhost"
        """
        return self.contents["connection_url"]

    @connection_url.setter
    def connection_url(self, value):
        self.contents["connection_url"] = value
        self.dump_configuration_to_yaml_file(self.contents)

    @property
    def enable_database_echo(self):
        return self.contents["enable_database_echo"]

    @enable_database_echo.setter
    def enable_database_echo(self, value):
        self.contents["enable_database_echo"] = value
        self.dump_configuration_to_yaml_file(self.contents)

    @property
    def enable_asynchronous_payload_delivery(self):
        return self.contents["enable_asynchronous_payload_delivery"]

    @enable_asynchronous_payload_delivery.setter
    def enable_asynchronous_payload_delivery(self, value):
        if sys.version_info[0:3] > (3, 8, 2) and value is True:
            self.contents["enable_asynchronous_payload_delivery"] = True
            self.dump_configuration_to_yaml_file(self.contents)

        else:
            self.contents["enable_asynchronous_payload_delivery"] = False
            self.dump_configuration_to_yaml_file(self.contents)

    @property
    def enable_auto_clean_up_old_test_results(self):
        return self.contents["enable_auto_clean_up_old_test_results"]

    @enable_auto_clean_up_old_test_results.setter
    def enable_auto_clean_up_old_test_results(self, value):
        self.contents["enable_auto_clean_up_old_test_results"] = value
        self.dump_configuration_to_yaml_file(self.contents)

    @property
    def max_number_saved_test_results(self):
        return self.contents["maximum_number_saved_test_results"]

    @max_number_saved_test_results.setter
    def max_number_saved_test_results(self, value):
        self.contents["maximum_number_saved_test_results"] = value
        self.dump_configuration_to_yaml_file(self.contents)


options = Configuration()
