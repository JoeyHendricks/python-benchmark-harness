from QuickPotato.configuration.management import options
from QuickPotato.database.management import SchemaManager
from sqlalchemy import select, func, and_


class Inserts(SchemaManager):

    def __init__(self):
        super(Inserts, self).__init__()

    def insert_performance_statistics(self, payload, database_name):
        """
        :return:
        """
        table = self.performance_statistics_schema()
        statement = table.insert()

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        connection.execute(statement, payload)

        connection.close()
        engine.dispose()

        return True

    def insert_system_resources_statistics(self, payload, database_name):
        """
        :return:
        """
        table = self.system_resources_schema()
        statement = table.insert()

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        connection.execute(statement, payload)

        connection.close()
        engine.dispose()

        return True

    def insert_boundaries_test_evidence(self, database_name, payload):
        """

        :param database_name:
        :param payload:
        :return:
        """
        table = self.boundaries_test_evidence_schema()
        statement = table.insert()

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        connection.execute(statement, payload)

        connection.close()
        engine.dispose()

        return True

    def insert_regression_test_evidence(self, database_name, payload):
        """
        If the regression test report does not exist in database.
        Then this method will create the first row.

        Note that all additional statistical tests will update this
        row with their payload if they are executed.

        Parameters
        ----------
        database_name: The name of the database
        payload: A dictionary payload which should contain the updated values

        Returns
        -------
        Will return True on success.
        """
        table = self.regression_test_evidence_schema()
        statement = table.insert()

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        connection.execute(statement, payload)

        connection.close()
        engine.dispose()

        return True

    def insert_results_into_test_report(self, database_name, payload):
        """
        If the regression test report does not exist in database.
        Then this method will create the first row.

        Note that all additional statistical tests will update this
        row with their payload if they are executed.

        Parameters
        ----------
        database_name: The name of the database
        payload: A dictionary payload which should contain the updated values

        Returns
        -------
        Will return True on success.
        """
        table = self.test_report_schema()
        statement = table.insert()

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        connection.execute(statement, payload)

        connection.close()
        engine.dispose()

        return True


class Select(SchemaManager):

    def __init__(self):
        super(Select, self).__init__()

    def select_end_to_end_response_times(self, database_name, test_id):
        """
        :param test_id:
        :param database_name:
        :return:
        """
        table = self.performance_statistics_schema()
        query = select([table.c.sample_id.distinct(), table.c.total_response_time]).where(table.c.test_id == test_id)

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        results = [float(row.total_response_time) for row in connection.execute(query)]

        connection.close()
        engine.dispose()

        return results

    def select_cumulative_time(self, database_name, test_id):
        """
        :param test_id:
        :param database_name:
        :return:
        """
        table = self.performance_statistics_schema()
        query = select([table.c.cumulative_time]).where(and_(table.c.test_id == test_id, table.c.cumulative_time > 0))

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        results = [float(row.cumulative_time) for row in connection.execute(query)]

        connection.close()
        engine.dispose()

        return results

    def select_all_call_stacks(self, database_name, test_id, alphabetical_order=False):
        """

        :param database_name:
        :param test_id:
        :param alphabetical_order:
        :return:
        """
        table = self.performance_statistics_schema()
        if alphabetical_order:
            query = table.select().where(table.c.test_id == test_id).order_by(table.c.function_name)
        else:
            query = table.select().where(table.c.test_id == test_id)
        results = []

        engine = self.spawn_engine(database_name)
        connection = engine.connect()

        for row in connection.execute(query):
            results.append(
                {
                    "id": row.id,
                    "test_id": row.test_id,
                    "test_case_name": database_name,
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

        connection.close()
        engine.dispose()

        return results

    def select_call_stack(self, database_name, sample_id):
        """

        Parameters
        ----------
        database_name
        sample_id

        Returns
        -------

        """
        table = self.performance_statistics_schema()
        query = table.select().where(table.c.sample_id == str(sample_id)).order_by(table.c.cumulative_time.desc())
        results = []

        engine = self.spawn_engine(database_name)
        connection = engine.connect()

        for row in connection.execute(query):
            results.append(
                {
                    "id": row.id,
                    "test_id": row.test_id,
                    "test_case_name": database_name,
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
        connection.close()
        engine.dispose()

        return results

    def select_all_test_ids(self, table, database_name, number=options.maximum_number_of_saved_test_results):
        """

        Parameters
        ----------
        table
        database_name
        number

        Returns
        -------

        """
        query = select([table.c.test_id]).distinct().limit(number)

        engine = self.spawn_engine(database_name)
        connection = engine.connect()

        results = [str(row.test_id) for row in connection.execute(query)]

        connection.close()
        engine.dispose()

        return results

    def select_all_meta_data(self, database_name, test_id):
        """

        Parameters
        ----------
        database_name
        test_id

        Returns
        -------

        """
        table = self.performance_statistics_schema()
        query = select([table.c.sample_id,
                        table.c.name_of_method_under_test,
                        table.c.human_timestamp,
                        table.c.total_response_time]).distinct().where(table.c.test_id == test_id)
        results = []

        engine = self.spawn_engine(database_name)
        connection = engine.connect()

        for row in connection.execute(query):
            results.append(
                {
                    "sample_id": row.sample_id,
                    "name_of_method_under_test": row.name_of_method_under_test,
                    "human_timestamp": row.human_timestamp,
                    "total_response_time": row.total_response_time
                }
            )

        connection.close()
        engine.dispose()

        return results

    def select_previous_test_id(self, database_name):
        """
        :param database_name:
        :return:
        """

        table = self.performance_statistics_schema()
        query = select([table.c.test_id]).distinct()

        engine = self.spawn_engine(database_name)
        connection = engine.connect()

        results = [str(row.test_id) for row in connection.execute(query)]
        connection.close()
        engine.dispose()

        return None if len(results) == 0 else results[-1]

    def select_previous_passed_test_id(self, database_name):
        """
        :param database_name:
        :return:
        """
        table = self.test_report_schema()
        query = select([table.c.test_id]).where(table.c.status == "1").order_by(table.c.id.desc()).limit(1)

        engine = self.spawn_engine(database_name)
        connection = engine.connect()

        results = [str(row.test_id) for row in connection.execute(query)]

        connection.close()
        engine.dispose()

        return results[0] if len(results) == 1 else None

    def select_total_number_of_test_ids(self, database_name):
        """
        :param database_name:
        :return:
        """
        table = self.performance_statistics_schema()
        query = select([func.count(table.c.test_id.distinct())])

        engine = self.spawn_engine(database_name)
        connection = engine.connect()

        results = int([row[0] for row in connection.execute(query)][0])

        connection.close()
        engine.dispose()

        return results


class Update(SchemaManager):

    def __init__(self):
        super(Update, self).__init__()

    def update_results_in_test_report(self, database_name, test_id, payload):
        """
        Updates the regression test report when and additional statistical test is performed.
        Parameters
        ----------
        payload: A dictionary payload which should contain the updated values
        database_name: The name of the database
        test_id: The test id which needs the update
        Returns
        -------
        Will return True on success
        """
        table = self.test_report_schema()
        statement = table.update().where(table.c.test_id == str(test_id)).values(payload)

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        connection.execute(statement)

        connection.close()
        engine.dispose()
        return True


class Delete(SchemaManager):

    def __init__(self):
        super(Delete, self).__init__()

    def delete_performance_statistics_that_match_test_id(self, database_name, test_id):
        """

        Parameters
        ----------
        database_name
        test_id

        Returns
        -------

        """
        table = self.performance_statistics_schema()
        query = table.delete().where(table.c.test_id == str(test_id))

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        connection.execute(query)

        connection.close()
        engine.dispose()
        return True


class DatabaseOperations(Inserts, Select, Delete, Update):

    def __init__(self):
        super(DatabaseOperations, self).__init__()

    def enforce_test_result_retention_policy(self, database_name):
        """
        :return:
        """
        current_number_of_test_ids = self.select_total_number_of_test_ids(database_name)
        maximum_number_of_test_ids = options.maximum_number_of_saved_test_results

        if current_number_of_test_ids > maximum_number_of_test_ids and \
                options.enable_auto_clean_up_old_test_results is True:

            oldest_test_ids = self.select_all_test_ids(
                table=self.performance_statistics_schema(),
                database_name=database_name,
                number=options.maximum_number_of_saved_test_results - 1
            )

            for test_id in oldest_test_ids:
                self.delete_performance_statistics_that_match_test_id(database_name, test_id)

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
        all_test_ids = self.select_all_test_ids(
            table=self.test_report_schema(),
            database_name=database_name,
            number=options.maximum_number_of_saved_test_results - 1
            )

        if test_id in all_test_ids:
            return True

        else:
            return False
