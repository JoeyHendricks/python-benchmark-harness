from .._database.common import CommonDatabaseInteractions
from .._utilities.defaults import default_sqlite_database_name
from .._configuration import options
from sqlalchemy import select, func
from tempfile import gettempdir


class Create(CommonDatabaseInteractions):

    def __init__(self):
        super(Create, self).__init__()

    def insert_performance_statistics(self, url: str, payload: list, tcn: str) -> None:
        """

        :param url:
        :param payload:
        :param tcn:
        :return:
        """
        return self.bulk_insert(
            connection_url=url,
            table=self.c_profiler_statistics_data_model(test_case_name=tcn),
            payload=payload
        )

    def insert_boundary_verification_results(self, url: str, payload: list, tcn: str) -> None:
        """

        :param url:
        :param payload:
        :param tcn:
        :return:
        """
        return self.bulk_insert(
            connection_url=url,
            table=self.boundary_test_report_model(test_case_name=tcn),
            payload=payload
        )


class Read(CommonDatabaseInteractions):

    def __init__(self):
        super(Read, self).__init__()

    def select_benchmark_profiled_method_response_times(self, url: str, tcn: str, test_id: float) -> list:
        """

        :param url:
        :param tcn:
        :param test_id:
        :return:
        """
        table = self.c_profiler_statistics_data_model(test_case_name=tcn)
        return [
            float(row.total_response_time) for row in self.execute_sql_statement(
                connection_url=url,
                query=select(
                    [
                        table.c.sample_id.distinct(),
                        table.c.total_response_time
                    ]
                ).where(table.c.test_id == test_id)
            )
        ]

    def select_benchmark_profiled_method_cumulative_latency(self, url: str, tcn: str, test_id: float) -> list:
        """

        :param url:
        :param tcn:
        :param test_id:
        :return:
        """
        table = self.c_profiler_statistics_data_model(test_case_name=tcn)
        return [
            float(row.cumulative_time) for row in self.execute_sql_statement(
                connection_url=url,
                query=select(
                    [
                        table.c.sample_id.distinct(),
                        table.c.cumulative_time
                    ]
                ).where(table.c.test_id == test_id)
            )
        ]

    def select_benchmarks_with_statistics(self, url: str, tcn: str, number=options.set_max_saved_tests) -> list:
        """

        :param url:
        :param tcn:
        :param number:
        :return:
        """
        table = self.c_profiler_statistics_data_model(test_case_name=tcn)
        return [
            float(row.test_id) for row in self.execute_sql_statement(
                connection_url=url,
                query=select([table.c.test_id]).distinct().limit(number).order_by(table.c.test_id.desc())
            )
        ]

    def select_validated_benchmarks(self, url: str, tcn: str, number=options.set_max_saved_tests) -> list:
        """

        :param url:
        :param tcn:
        :param number:
        :return:
        """
        table = self.boundary_test_report_model(test_case_name=tcn)
        return [
            str(row.test_id) for row in self.execute_sql_statement(
                connection_url=url,
                query=select([table.c.test_id]).distinct().limit(number)
            )
        ]

    def select_count_of_all_available_benchmarks(self, url: str, tcn: str) -> int:
        """

        :param url:
        :param tcn:
        :return:
        """
        table = self.c_profiler_statistics_data_model(test_case_name=tcn)
        return int(
            [
                row[0] for row in self.execute_sql_statement(
                    connection_url=url,
                    query=select([func.count(table.c.test_id.distinct())])
                )
            ]
            [0]
        )

    def select_benchmark_call_stack_by_sample_id(self, url: str, tcn: str, sample_id: str) -> list:
        """

        :param url:
        :param tcn:
        :param sample_id:
        :return:
        """
        table = self.c_profiler_statistics_data_model(test_case_name=tcn)
        return [
            {
                "uuid": row.uuid,
                "test_id": row.test_id,
                "test_case_name": row.test_case_name,
                "sample_id": row.sample_id,
                "name_of_method_under_test": row.name_of_method_under_test,
                "epoch_timestamp": int(row.epoch_timestamp),
                "human_timestamp": row.human_timestamp,
                "child_path": row.child_path,
                "child_line_number": row.child_line_number,
                "child_function_name": row.child_function_name,
                "parent_path": row.parent_path,
                "parent_line_number": row.parent_line_number,
                "parent_function_name": row.parent_function_name,
                "number_of_calls": row.number_of_calls,
                "total_time": float(row.total_time),
                "cumulative_time": float(row.cumulative_time),
                "total_response_time": float(row.total_response_time)
            }
            for row in self.execute_sql_statement(
                connection_url=url,
                query=table.select().where(
                    table.c.sample_id == str(sample_id)
                ).order_by(
                    table.c.cumulative_time.desc()
                )
            )
        ]

    def select_benchmark_call_stack_by_test_id(self, url: str, tcn: str, test_id: float) -> list:
        """

        :param url:
        :param tcn:
        :param test_id:
        :return:
        """
        table = self.c_profiler_statistics_data_model(test_case_name=tcn)
        return [
            {
                "uuid": row.uuid,
                "test_id": row.test_id,
                "test_case_name": row.test_case_name,
                "sample_id": row.sample_id,
                "name_of_method_under_test": row.name_of_method_under_test,
                "epoch_timestamp": int(row.epoch_timestamp),
                "human_timestamp": row.human_timestamp,
                "child_path": row.child_path,
                "child_line_number": row.child_line_number,
                "child_function_name": row.child_function_name,
                "parent_path": row.parent_path,
                "parent_line_number": row.parent_line_number,
                "parent_function_name": row.parent_function_name,
                "number_of_calls": row.number_of_calls,
                "total_time": float(row.total_time),
                "cumulative_time": float(row.cumulative_time),
                "total_response_time": float(row.total_response_time)
            }
            for row in self.execute_sql_statement(
                connection_url=url,
                query=table.select().where(
                    table.c.test_id == str(test_id)
                ).order_by(
                    table.c.cumulative_time.desc()
                )
            )
        ]

    def select_all_sample_ids_in_benchmark_by_test_id(self, url: str, tcn: str, test_id: float) -> list:
        """

        :param url:
        :param tcn:
        :param test_id:
        :return:
        """
        table = self.c_profiler_statistics_data_model(test_case_name=tcn)
        return [
            str(row.sample_id) for row in self.execute_sql_statement(
                connection_url=url,
                query=select(
                    [
                        table.c.sample_id
                    ]
                ).where(
                    table.c.test_id == test_id
                ).distinct()
            )
        ]


class Delete(CommonDatabaseInteractions):

    def __init__(self):
        super(Delete, self).__init__()

    def delete_performance_statistics_that_match_test_id(self, url: str, tcn: str, test_id: float) -> None:
        """

        :param url:
        :param tcn:
        :param test_id:
        :return:
        """
        table = self.c_profiler_statistics_data_model(test_case_name=tcn)
        self.execute_sql_statement(
            connection_url=url,
            query=table.delete().where(table.c.test_id == str(test_id))
        )


class Crud(Create, Read, Delete):

    def __init__(self):
        super(Crud, self).__init__()

    @staticmethod
    def _create_default_db_url():
        """

        :return:
        """
        temp_directory = gettempdir()
        separator = "\\" if '\\' in gettempdir() else "/"
        return "sqlite:///" + temp_directory + separator + default_sqlite_database_name + ".db"

    def _enforce_data_retention_policy(self, url: str, tcn: str) -> None:
        """

        :param url:
        :param tcn:
        :return:
        """
        current_number_of_test_ids = self.select_count_of_all_available_benchmarks(url, tcn)
        maximum_number_of_test_ids = options.set_max_saved_tests

        if current_number_of_test_ids > maximum_number_of_test_ids and \
                options.enable_auto_clean_up_old_test_results is True:

            oldest_test_ids = self.select_benchmarks_with_statistics(
                url=url,
                tcn=tcn,
                number=options.set_max_saved_tests - 1
            )

            for test_id in oldest_test_ids:
                self.delete_performance_statistics_that_match_test_id(
                    url=url,
                    tcn=tcn,
                    test_id=test_id
                )

    def _verify_and_create_relevant_tables_in_database(self, url: str, tcn: str) -> None:
        """

        :param url:
        :param tcn:
        :return:
        """
        # Models that need to be available in the _database
        models = [
            self.c_profiler_statistics_data_model(test_case_name=tcn),
            self.boundary_test_report_model(test_case_name=tcn)
        ]
        for table_model in models:

            # verify if relevant table exists
            if self.check_if_table_exists(connection_url=url, table_name=str(table_model.name)):
                continue

            # table does not exist creating it in _database
            else:
                self.spawn_table(
                    connection_url=url,
                    model=table_model
                )
