from QuickPotato.configuration.management import options
from QuickPotato.database.schemas import *
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from QuickPotato.utilities.exceptions import *
from sqlalchemy_utils import database_exists, create_database, drop_database
import tempfile


class StatementManager(RawStatisticsSchemas, UnitPerformanceTestResultSchemas):

    URL = options.connection_url

    def __init__(self):
        RawStatisticsSchemas.__init__(self)
        UnitPerformanceTestResultSchemas.__init__(self)

    def spawn_session(self, database_name):
        """
        :return:
        """
        try:
            url = self._validate_connection_url(database_name=database_name)
            engine = create_engine(url, echo=options.enable_database_echo)
            return engine

        except Exception:
            raise DatabaseConnectionCannotBeSpawned()

    def execute_query(self, database, query):
        """

        :param database:
        :param query:
        :return:
        """
        # Set-up connection
        engine = self.spawn_session(database)
        connection = engine.connect()

        # Run query
        results = connection.execute(query)

        # Close connection
        connection.close()
        engine.dispose()
        return results

    def create_schema(self, database, schema):
        """

        :param database:
        :param schema:
        :return:
        """
        engine = self.spawn_session(database)
        schema.metadata.create_all(engine)
        engine.dispose()
        return True

    def create_database(self, database_name):
        """

        :param database_name:
        :return:
        """
        try:
            # Add check for SQLite
            engine = self.spawn_session(database_name)
            if not database_exists(engine.url):
                create_database(engine.url)
            engine.dispose()
            return True

        except ProgrammingError:
            # Database exists no need to re-create it
            return True

        except Exception:
            raise DatabaseSchemaCannotBeSpawned()

    def delete_database(self, database_name):
        """

        :param database_name:
        :return:
        """
        engine = self.spawn_session(database_name)
        if database_exists(engine.url):
            drop_database(engine.url)
        return True

    def _validate_connection_url(self, database_name):
        """
        :return:
        """
        if self.URL is None:
            path = tempfile.gettempdir()
            path = path + "\\" if '\\' in path else path + "/"
            return "sqlite:///" + path + database_name + ".db"

        elif options.connection_url.startswith('sqlite'):
            return self.URL + database_name + ".db"

        else:
            return f"{self.URL}/{database_name}"
