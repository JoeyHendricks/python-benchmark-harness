from Benchmarking._database.collection import Crud
from Benchmarking._utilities.exceptions import UnableToExportVisualization
from datetime import datetime
import pandas as pd
import os


class CsvFile(Crud):

    def __init__(self, test_case_name: str, test_id: str, database_connection_url=None, delimiter=","):
        """
        Will build up the object, when no test id is given and when test case name is default.
        It will take the last known test id.

        :param test_case_name: The name of the test case
        :param delimiter: The delimiter of the csv file
        :param database_connection_url: the connection url to the _database
        :param test_id: The test id within the test case
        """
        super(CsvFile, self).__init__()
        self.test_case_name = test_case_name
        self._url = self._create_default_db_url() if database_connection_url is None else database_connection_url
        self.delimiter = delimiter
        self.test_id = test_id
        self.list_of_samples = self.select_all_sample_ids_in_benchmark_by_test_id(
            url=self._url,
            tcn=test_case_name,
            test_id=test_id
        )

    def export(self, path):
        """
        Will export the csv file to a directory on the disk.
        :param path: The path on disk where the file needs to be written.
                     Example: C:\\temp\\
        """
        if os.path.isdir(path):
            content = []
            for sample_id in self.list_of_samples:
                stack = self.select_benchmark_call_stack_by_sample_id(
                    url=self._url,
                    tcn=self.test_case_name,
                    sample_id=sample_id
                )
                for line in stack:
                    content.append(line)

            pd.DataFrame(content).to_csv(
                path_or_buf=f"{path}raw_export_of_{self.test_id}_{str(datetime.now().timestamp())}.csv",
                sep=self.delimiter,
                index=False
            )

        else:
            raise UnableToExportVisualization()
