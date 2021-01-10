from sqlalchemy import select, func
from QuickPotato.database.operations import StatementManager
from QuickPotato.configuration.management import options


class Create(StatementManager):

    def __init__(self):
        super(Create, self).__init__()

    def insert_performance_statistics(self, database, payload):
        """

        :param database:
        :param payload:
        :return:
        """
        table = self.performance_statistics_schema()
        engine, connection = self.spawn_connection(database)
        self.execute_query(connection, query=table.insert().values(payload))
        self.close_connection(engine, connection)
        return True

    def insert_system_resources_statistics(self, database, payload):
        """

        :param database:
        :param payload:
        :return:
        """
        table = self.system_resources_schema()
        engine, connection = self.spawn_connection(database)
        self.execute_query(connection, query=table.insert().values(payload))
        self.close_connection(engine, connection)
        return True

    def insert_boundaries_test_evidence(self, database, payload):
        """

        :param database:
        :param payload:
        :return:
        """
        table = self.boundaries_test_evidence_schema()
        engine, connection = self.spawn_connection(database)
        self.execute_query(connection, query=table.insert().values(payload))
        self.close_connection(engine, connection)
        return True

    def insert_regression_test_evidence(self, database, payload):
        """

        :param database:
        :param payload:
        :return:
        """
        table = self.regression_test_evidence_schema()
        engine, connection = self.spawn_connection(database)
        self.execute_query(connection, query=table.insert().values(payload))
        self.close_connection(engine, connection)
        return True

    def insert_results_into_test_report(self, database, payload):
        """

        :param database:
        :param payload:
        :return:
        """
        table = self.test_report_schema()
        engine, connection = self.spawn_connection(database)
        self.execute_query(connection, query=table.insert().values(payload))
        self.close_connection(engine, connection)
        return True

    def spawn_performance_statistics_schema(self, database):
        """

        :param database:
        :return:
        """
        self.create_schema(database, self.performance_statistics_schema())
        return True

    def spawn_system_resources_schema(self, database):
        """

        :param database:
        :return:
        """
        self.create_schema(database, self.system_resources_schema())
        return True

    def spawn_test_report_schema(self, database):
        """

        :param database:
        :return:
        """
        self.create_schema(database, self.test_report_schema())
        return True

    def spawn_boundaries_test_evidence_schema(self, database):
        """

        :param database:
        :return:
        """
        self.create_schema(database, self.boundaries_test_evidence_schema())
        return True

    def spawn_regression_test_evidence_schema(self, database):
        """

        :param database:
        :return:
        """
        self.create_schema(database, self.regression_test_evidence_schema())
        return True

    def spawn_result_database(self, database_name):
        """

        :param database_name:
        :return:
        """
        self.create_database(database_name)
        return True


class Read(StatementManager):

    def __init__(self):
        super(Read, self).__init__()

    def select_response_times(self, database, test_id):
        """

        :param database:
        :param test_id:
        :return:
        """
        table = StatementManager.performance_statistics_schema()
        engine, connection = self.spawn_connection(database)
        query = select([table.c.sample_id.distinct(), table.c.total_response_time]).where(table.c.test_id == test_id)
        results = [float(row.total_response_time) for row in self.execute_query(connection, query)]
        self.close_connection(engine, connection)
        return results

    def select_test_ids_with_performance_statistics(self, database, number=options.maximum_number_saved_test_results):
        """

        :param database:
        :param number:
        :return:
        """
        table = StatementManager.performance_statistics_schema()
        engine, connection = self.spawn_connection(database)
        query = select([table.c.test_id]).distinct().limit(number)
        results = [str(row.test_id) for row in self.execute_query(connection, query)]
        self.close_connection(engine, connection)
        return results

    def select_validated_test_ids(self, database, number=options.maximum_number_saved_test_results):
        """

        :param database:
        :param number:
        :return:
        """
        table = StatementManager.test_report_schema()
        engine, connection = self.spawn_connection(database)
        query = select([table.c.test_id]).distinct().limit(number)
        results = [str(row.test_id) for row in self.execute_query(connection, query)]
        self.close_connection(engine, connection)
        return results

    def select_previous_test_id(self, database):
        """

        :param database:
        :return:
        """
        table = StatementManager.performance_statistics_schema()
        engine, connection = self.spawn_connection(database)
        query = select([table.c.test_id]).distinct()
        results = [str(row.test_id) for row in self.execute_query(connection, query)]
        self.close_connection(engine, connection)
        return None if len(results) == 0 else results[-1]

    def select_previous_passed_test_id(self, database):
        """

        :param database:
        :return:
        """
        table = StatementManager.test_report_schema()
        engine, connection = self.spawn_connection(database)
        query = select([table.c.test_id]).where(table.c.status == "1").order_by(table.c.id.desc()).limit(1)
        results = [str(row.test_id) for row in self.execute_query(connection, query)]
        self.close_connection(engine, connection)
        return results[0] if len(results) == 1 else None

    def select_count_of_test_ids(self, database):
        """

        :param database:
        :return:
        """
        table = StatementManager.performance_statistics_schema()
        engine, connection = self.spawn_connection(database)
        query = select([func.count(table.c.test_id.distinct())])
        results = int([row[0] for row in self.execute_query(connection, query)][0])
        self.close_connection(engine, connection)
        return results

    def select_call_stack_by_sample_id(self, database, sample_id):
        """

        :param database:
        :param sample_id:
        :return:
        """
        table = StatementManager.performance_statistics_schema()
        engine, connection = self.spawn_connection(database)
        query = table.select().where(table.c.sample_id == str(sample_id)).order_by(table.c.cumulative_time.desc())

        results = []
        for row in self.execute_query(connection, query):
            results.append(
                {
                    "id": row.id,
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
            )
        self.close_connection(engine, connection)
        return results

    def select_call_stacks_by_test_id(self, database, test_id):
        """
        :param database:
        :param test_id:
        :return:
        """
        table = self.performance_statistics_schema()
        query = table.select().where(table.c.test_id == test_id)
        engine, connection = self.spawn_connection(database)

        results = []
        for row in self.execute_query(connection, query):
            results.append(
                {
                    "id": row.id,
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
            )
        self.close_connection(engine, connection)
        return results

    def select_test_id_description(self, database, test_id):
        """

        :param database:
        :param test_id:
        :return:
        """
        table = StatementManager.performance_statistics_schema()
        query = select([table.c.sample_id,
                        table.c.name_of_method_under_test,
                        table.c.human_timestamp,
                        table.c.total_response_time]).distinct().where(table.c.test_id == test_id)
        engine, connection = self.spawn_connection(database)

        results = []
        for row in self.execute_query(connection, query):
            results.append(
                {
                    "sample_id": row.sample_id,
                    "name_of_method_under_test": row.name_of_method_under_test,
                    "human_timestamp": row.human_timestamp,
                    "total_response_time": row.total_response_time
                }
            )
        self.close_connection(engine, connection)
        return results


class Update(StatementManager):

    def __init__(self):
        super(Update, self).__init__()

    def update_results_in_test_report(self, database, test_id, payload):
        """

        :param database:
        :param test_id:
        :param payload:
        :return:
        """
        table = StatementManager.test_report_schema()
        query = table.update().where(table.c.test_id == str(test_id)).values(payload)
        engine, connection = self.spawn_connection(database)
        results = self.execute_query(connection, query)
        self.close_connection(engine, connection)
        return results


class Delete(StatementManager):

    def __init__(self):
        super(Delete, self).__init__()

    def delete_performance_statistics_that_match_test_id(self, database, test_id):
        """

        :param database:
        :param test_id:
        :return:
        """
        table = StatementManager.performance_statistics_schema()
        query = table.delete().where(table.c.test_id == str(test_id))
        engine, connection = self.spawn_connection(database)
        results = self.execute_query(connection, query)
        self.close_connection(engine, connection)
        return results

    def delete_result_database(self, database_name):
        """

        :param database_name:
        :return:
        """
        self.delete_database(database_name)
        return True


class Crud(Create, Read, Update, Delete):

    def __init__(self):
        super(Crud, self).__init__()

    def enforce_test_result_retention_policy(self, database):
        """

        :param database:
        :return:
        """
        current_number_of_test_ids = self.select_count_of_test_ids(database)
        maximum_number_of_test_ids = options.maximum_number_saved_test_results

        if current_number_of_test_ids > maximum_number_of_test_ids and \
                options.enable_auto_clean_up_old_test_results is True:

            oldest_test_ids = self.select_test_ids_with_performance_statistics(
                database=database,
                number=options.maximum_number_saved_test_results - 1
            )

            for test_id in oldest_test_ids:
                self.delete_performance_statistics_that_match_test_id(database, test_id)

        return True

    def check_if_test_id_exists_in_test_report(self, database_name, test_id):
        """
        This method finds out if the test report needs to be updated or created.
        Parameters
        ----------
        database_name: the name of the database (This is equal to the test case)
        test_id: The tests id that needs to be found.
        Returns
        -------
        When test id is found it will output True, if not it will output False
        """
        all_test_ids = self.select_validated_test_ids(
            database=database_name,
            number=options.maximum_number_saved_test_results - 1
            )

        if test_id in all_test_ids:
            return True

        else:
            return False
