from os.path import isfile, dirname, realpath
from QuickPotato.utilities.templates import default_quick_potato_configuration
import yaml


class Configuration:

    FILE_NAME = "options.yaml"
    PATH = dirname(realpath(__file__)) + "\\" if "\\" in dirname(realpath(__file__)) else dirname(realpath(__file__)) + "/"

    def __init__(self):

        if isfile(self.PATH + self.FILE_NAME) is False:
            self.dump_setting_to_yaml_file(default_quick_potato_configuration)

        self.contents = yaml.safe_load(open(self.PATH + self.FILE_NAME))

    def dump_setting_to_yaml_file(self, contents):

        with open(self.PATH + self.FILE_NAME, 'w') as file:
            yaml.dump(contents, file)

    @property
    def collect_performance_statistics(self):
        return self.contents["collect_performance_statistics"]

    @collect_performance_statistics.setter
    def collect_performance_statistics(self, value):
        self.contents["collect_performance_statistics"] = value
        self.dump_setting_to_yaml_file(self.contents)

    @property
    def database_connection_url(self):
        """Specify which database vendor you want to use.
        For SQLite: "sqlite:///C:\\temp\\"
        For MySQL:  "mysql+pymysql://user:password@localhost"
        """
        return self.contents["database_connection_url"]

    @database_connection_url.setter
    def database_connection_url(self, value):
        self.contents["database_connection_url"] = value
        self.dump_setting_to_yaml_file(self.contents)

    @property
    def database_echo(self):
        return self.contents["database_echo"]

    @database_echo.setter
    def database_echo(self, value):
        self.contents["database_echo"] = value
        self.dump_setting_to_yaml_file(self.contents)

    @property
    def asynchronous_payload_delivery(self):
        return self.contents["asynchronous_payload_delivery"]

    @asynchronous_payload_delivery.setter
    def asynchronous_payload_delivery(self, value):
        self.contents["asynchronous_payload_delivery"] = value
        self.dump_setting_to_yaml_file(self.contents)

    @property
    def automatically_clean_up_old_test_results(self):
        return self.contents["automatically_clean_up_old_test_results"]

    @automatically_clean_up_old_test_results.setter
    def automatically_clean_up_old_test_results(self, value):
        self.contents["automatically_clean_up_old_test_results"] = value
        self.dump_setting_to_yaml_file(self.contents)

    @property
    def maximum_number_of_saved_test_results(self):
        return self.contents["maximum_number_of_saved_test_results"]

    @maximum_number_of_saved_test_results.setter
    def maximum_number_of_saved_test_results(self, value):
        self.contents["maximum_number_of_saved_test_results"] = value
        self.dump_setting_to_yaml_file(self.contents)


options = Configuration()
