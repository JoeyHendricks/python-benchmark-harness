from CouchPotato.database.queries import Crud
from CouchPotato.configuration.management import options
from sqlalchemy_utils import database_exists
from sqlalchemy import create_engine
from example.example_code import *
import unittest

SAMPLE_SIZE = 1
UNIT_TEST_DATABASE_NAME = "quickprofiling"


class TestUsage(unittest.TestCase):

    def setUp(self):
        """

        """
        options.enable_intrusive_profiling = True

    def tearDown(self):
        """

        """
        options.enable_intrusive_profiling = False
        self.clean_up_database()

    @staticmethod
    def clean_up_database():
        """

        """
        database_manager = Crud()
        database_manager.delete_result_database(UNIT_TEST_DATABASE_NAME)

    def test_profiling_outside_of_test_case(self):

        for _ in range(0, SAMPLE_SIZE):
            fast_method()

        # Checking if a database has been spawned
        database_manager = Crud()
        url = database_manager._validate_connection_url(UNIT_TEST_DATABASE_NAME)
        engine = create_engine(url, echo=True)

        self.assertTrue(database_exists(engine.url))
