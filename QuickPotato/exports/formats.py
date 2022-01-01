from QuickPotato.database.collection import Crud
from QuickPotato.utilities.exceptions import UnableToGenerateVisualizations, \
    UnableToExportVisualization
from datetime import datetime
import pandas as pd
import os


class CsvFile(Crud):

    def __init__(self, test_case_name=default_test_case_name, database_name=default_database_name,
                 test_id=None, delimiter=","):
        """
        Will build up the object, when no test id is given and when test case name is default.
        It will take the last known test id.

        :param test_case_name: The name of the test case
        :param delimiter: The delimiter of the csv file
        :param database_name:
        :param test_id: The test id within the test case
        """
        super(CsvFile, self).__init__()
        self.test_case_name = test_case_name
        self.database_name = database_name
        self.delimiter = delimiter
        self.test_id = test_id

        if self.test_id is None:
            raise UnableToGenerateVisualizations()

        self.list_of_samples = self.select_all_sample_ids(
            database_name=self.database_name,
            test_id=self.test_id
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
                stack = self.select_call_stack_by_sample_id(
                    database_name=self.database_name,
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