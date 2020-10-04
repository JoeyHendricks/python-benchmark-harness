from os.path import isfile, dirname, realpath
from QuickPotato.utilities.templates import default_quick_potato_configuration
import yaml


class Configuration:

    FILE_NAME = "options.yaml"
    PATH = dirname(realpath(__file__)) + "\\" if "\\" in dirname(realpath(__file__)) else dirname(realpath(__file__)) + "/"

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
    def enable_system_resource_collection(self):
        return self.contents["enable_system_resource_collection"]

    @enable_system_resource_collection.setter
    def enable_system_resource_collection(self, value):
        self.contents["enable_system_resource_collection"] = value
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
        self.contents["enable_asynchronous_payload_delivery"] = value
        self.dump_configuration_to_yaml_file(self.contents)

    @property
    def enable_auto_clean_up_old_test_results(self):
        return self.contents["enable_auto_clean_up_old_test_results"]

    @enable_auto_clean_up_old_test_results.setter
    def enable_auto_clean_up_old_test_results(self, value):
        self.contents["enable_auto_clean_up_old_test_results"] = value
        self.dump_configuration_to_yaml_file(self.contents)

    @property
    def maximum_number_of_saved_test_results(self):
        return self.contents["maximum_number_of_saved_test_results"]

    @maximum_number_of_saved_test_results.setter
    def maximum_number_of_saved_test_results(self, value):
        self.contents["maximum_number_of_saved_test_results"] = value
        self.dump_configuration_to_yaml_file(self.contents)


options = Configuration()
