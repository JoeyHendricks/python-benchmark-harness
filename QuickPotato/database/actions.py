from QuickPotato.configuration.manager import options
from QuickPotato.database.management import DatabaseManager
from sqlalchemy import select, func, and_
import pandas as pd


class Inserts(DatabaseManager):

    def __init__(self):
        super(Inserts, self).__init__()

    def insert_time_spent_statistics(self, payload, database_name):
        """
        :return:
        """
        table = self.time_spent_model()
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
        table = self.system_resources_model()
        statement = table.insert()

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        connection.execute(statement, payload)

        connection.close()
        engine.dispose()

        return True

    def insert_boundaries_test_report(self, payload, database_name):
        """
        :return:
        """
        table = self.boundaries_test_report_model()
        statement = table.insert()

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        connection.execute(statement, payload)

        connection.close()
        engine.dispose()

        return True

    def insert_regression_test_report(self, payload, database_name):
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
        table = self.regression_test_report_model()
        statement = table.insert()

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        connection.execute(statement, payload)

        connection.close()
        engine.dispose()

        return True


class Select(DatabaseManager):

    def __init__(self):
        super(Select, self).__init__()

    def select_end_to_end_response_times(self, database_name, test_id):
        """
        :param test_id:
        :param database_name:
        :return:
        """
        table = self.time_spent_model()
        query = select([table.c.uuid.distinct(), table.c.overall_response_time]).where(table.c.test_id == test_id)

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        results = [float(row.overall_response_time) for row in connection.execute(query)]

        connection.close()
        engine.dispose()

        return results

    def select_cumulative_time(self, database_name, test_id):
        """
        :param test_id:
        :param database_name:
        :return:
        """
        table = self.time_spent_model()
        query = select([table.c.cumulative_time]).where(and_(table.c.test_id == test_id, table.c.cumulative_time > 0))

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        results = [float(row.cumulative_time) for row in connection.execute(query)]

        connection.close()
        engine.dispose()

        return results

    def select_all_stacks(self, database_name, test_id):
        """
        :param test_id:
        :param database_name:
        :return:
        """
        table = self.time_spent_model()
        query = table.select().where(table.c.test_id == test_id)
        results = []

        engine = self.spawn_engine(database_name)
        connection = engine.connect()

        for row in connection.execute(query):
            results.append(
                {
                    "ID": row.ID,
                    "test_id": row.test_id,
                    "test_case_name": row.test_case_name,
                    "uuid": row.uuid,
                    "name_of_method_under_test": row.name_of_method_under_test,
                    "epoch_timestamp": row.epoch_timestamp,
                    "human_timestamp": row.human_timestamp,
                    "number_of_calls": row.number_of_calls,
                    "overall_response_time": row.overall_response_time,
                    "total_time": row.total_time,
                    "total_time_per_call": row.total_time_per_call,
                    "cumulative_time": row.cumulative_time,
                    "cumulative_time_per_call": row.cumulative_time_per_call,
                    "file": row.file,
                    "line_number": row.line_number,
                    "function_name": row.function_name
                }
            )

        connection.close()
        engine.dispose()

        return pd.DataFrame(results)

    def select_stack(self, database_name, stack_uuid):
        """

        Parameters
        ----------
        database_name
        stack_uuid

        Returns
        -------

        """
        table = self.time_spent_model()
        query = table.select().where(table.c.uuid == str(stack_uuid))
        results = []

        engine = self.spawn_engine(database_name)
        connection = engine.connect()

        for row in connection.execute(query):
            results.append(
                {
                    "test_id": row.test_id, "uuid": row.uuid,
                    "name_of_method_under_test": row.name_of_method_under_test,
                    "response_time": row.response_time, "epoch_datetime": row.epoch_datetime,
                    "human_datetime": row.human_datetime, "number_of_calls": row.number_of_calls,
                    "total_time": row.total_time, "total_time_per_call": row.total_time_per_call,
                    "cumulative_time": row.cumulative_time,
                    "cumulative_time_per_call": row.cumulative_time_per_call, "file": row.file,
                    "line_number": row.line_number, "function_name": row.function_name
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

    def select_previous_test_id(self, database_name):
        """
        :param database_name:
        :return:
        """

        table = self.time_spent_model()
        query = select([table.c.test_id]).distinct()

        engine = self.spawn_engine(database_name)
        connection = engine.connect()

        results = [str(row.test_id) for row in connection.execute(query)]
        connection.close()
        engine.dispose()
        
        if len(results) > 0:
            return results[-1]

        else:
            return None

    def select_total_number_of_test_ids(self, database_name):
        """
        :param database_name:
        :return:
        """
        table = self.time_spent_model()
        query = select([func.count(table.c.test_id.distinct())])

        engine = self.spawn_engine(database_name)
        connection = engine.connect()

        results = int([row[0] for row in connection.execute(query)][0])

        connection.close()
        engine.dispose()

        return results


class Delete(DatabaseManager):

    def __init__(self):
        super(Delete, self).__init__()

    def delete_time_spent_statistics_that_match_test_id(self, database_name, test_id):
        """

        Parameters
        ----------
        database_name
        test_id

        Returns
        -------

        """
        table = self.time_spent_model()
        query = table.delete().where(table.c.test_id == str(test_id))

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        connection.execute(query)

        connection.close()
        engine.dispose()
        return True


class Update(DatabaseManager):

    def __init__(self):
        super(Update, self).__init__()

    def update_regression_test_report(self, payload, test_id, database_name):
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
        table = self.regression_test_report_model()
        statement = table.update().where(table.c.test_id == str(test_id)).values(payload)

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        connection.execute(statement)

        connection.close()
        engine.dispose()
        return True

    def update_boundaries_test_report(self, payload, test_id, database_name):
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
        table = self.boundaries_test_report_model()
        statement = table.update().where(table.c.test_id == str(test_id)).values(payload)

        engine = self.spawn_engine(database_name)
        connection = engine.connect()
        connection.execute(statement)

        connection.close()
        engine.dispose()
        return True


class DatabaseActions(Inserts, Select, Delete, Update):

    def __init__(self):
        super(DatabaseActions, self).__init__()

    def enforce_test_result_retention_policy(self, database_name):
        """
        :return:
        """
        current_number_of_test_ids = self.select_total_number_of_test_ids(database_name)
        maximum_number_of_test_ids = options.maximum_number_of_saved_test_results

        if current_number_of_test_ids > maximum_number_of_test_ids and \
                options.automatically_clean_up_old_test_results is True:

            oldest_test_ids = self.select_all_test_ids(
                table=self.time_spent_model(),
                database_name=database_name,
                number=options.maximum_number_of_saved_test_results - 1
            )

            for test_id in oldest_test_ids:
                self.delete_time_spent_statistics_that_match_test_id(database_name, test_id)

        return True

    def check_if_test_id_exists_in_test_report(self, test_id, table, database_name):
        """
        This method finds out if the test report needs to be updated or created.

        Parameters
        ----------
        database_name: the name of the database (This is equal to the test case)
        test_id: The tests id that needs to be found.
        table: The name of the table.

        Returns
        -------
        When test id is found it will output True, if not it will output False
        """
        all_test_ids = self.select_all_test_ids(
            table=table,
            database_name=database_name,
            number=options.maximum_number_of_saved_test_results - 1
            )

        if test_id in all_test_ids:
            return True

        else:
            return False
