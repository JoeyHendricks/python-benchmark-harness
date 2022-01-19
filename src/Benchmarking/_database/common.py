from .._database.models import TableModels
from sqlalchemy_utils import database_exists
from sqlalchemy.engine import create_engine
from sqlalchemy import inspect


class CommonDatabaseContextManager(TableModels):

    @staticmethod
    def spawn_engine(connection_url: str) -> object:
        """
        Will spawn and engine which can be used to control the target _database.
        :param connection_url: The connection url
        :return: an SQLAlchemy engine object to create a connection
        """
        return create_engine(
            connection_url,
            echo=False,
            max_identifier_length=128
        )

    @staticmethod
    def close_connection(connection: object) -> None:
        """
        Will close the connection and give it back to the connection pool.
        :param connection: The active connection object.
        """
        connection.close()

    @staticmethod
    def execute(connection: object, payload: list, bulk_insert=False) -> tuple:
        """
        Will shoot a SQLAlchemy query or raw sql over an active SQL connection.
        :param bulk_insert:
        :param connection: An open connection object.
        :param payload: The payload either a SQLAlchemy statement or query
        :return: The results object.
        """
        if bulk_insert:
            connection.execute(payload[0], payload[1])

        else:
            return connection.execute(payload)

    def check_if_table_exists(self, connection_url: str, table_name: str) -> bool:
        """
        Will verify if a table exists in the target _database
        :param connection_url: The connection url
        :param table_name:
        :return: a bool which is either true or false
        """
        inspector = inspect(
            self.spawn_engine(
                connection_url
            )
        )
        tables_in_db = inspector.get_table_names()
        return True if table_name in tables_in_db else False

    def check_if_database_exists(self, connection_url: str) -> bool:
        """
        Will verify if a table exists in the target _database platform.
        :param connection_url: The connection url.
        :return: a bool which is either true or false
        """
        engine = self.spawn_engine(connection_url)
        return database_exists(repr(engine.url))

    def spawn_table(self, connection_url: str, model: object) -> None:
        """
        Spawn an table in the target _database.
        :param connection_url: The connection url
        :param model: The table schema which is used to describe the table.
        :return:
        """
        engine = self.spawn_engine(connection_url)
        model.metadata.create_all(engine)
        engine.dispose()

    def drop_table(self, connection_url: str, schema: object) -> None:
        """
        Drop a table in the target _database.
        :param connection_url: The connection url
        :param schema: The table schema which is used to describe the table.
        :return:
        """
        engine = self.spawn_engine(connection_url)
        schema.drop(engine)
        engine.dispose()

    def spawn_connection(self, connection_url) -> tuple:
        """
        Will spawn an connection to the _database.
        :param connection_url: The connection url
        :return: An active connection.
        """
        engine = self.spawn_engine(connection_url)
        return engine, engine.connect()


class CommonDatabaseInteractions(CommonDatabaseContextManager):

    def execute_sql_statement(self, connection_url: str, query: object) -> list:
        """
        Will perform an generic execute_sql_statement statement on the selected _database
        and return the results object.
        :return: an sqlalchemy results object.
        """
        # Creating connection
        engine, connection = self.spawn_connection(connection_url)

        # Executing statement and binding results to variable
        results = [row for row in self.execute(connection, query)]

        # Closing connection
        self.close_connection(connection)
        return results

    def bulk_insert(self, connection_url: str, table: object, payload: list) -> None:
        """
        Will use bulk bulk_insert to bulk_insert data into a _database.
        :param table: The table where the data needs to go.
        :param connection_url: The connection url
        :param payload: A list of dictionaries that gets inserted into a _database.
        """
        # Creating connection
        engine, connection = self.spawn_connection(connection_url)

        # Building bulk_insert command.
        statement = table.insert()

        # Executing inserting payload.
        self.execute(connection, [statement, payload], bulk_insert=True)

        # Closing connection.
        self.close_connection(connection)
