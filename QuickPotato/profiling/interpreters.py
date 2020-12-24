from QuickPotato.database.queries import Crud
from QuickPotato.utilities.exceptions import *
from QuickPotato.configuration.management import options
from datetime import datetime
import asyncio


class PerformanceStatisticsInterpreter(Crud):

    def __init__(self, database_name, performance_statistics, total_response_time, method_name, sample_id, test_id):
        super(PerformanceStatisticsInterpreter, self).__init__()

        self.performance_statistics = performance_statistics
        self.total_response_time = total_response_time
        self.using_server_less_database = bool(self._validate_connection_url(database_name)[0:6] == "sqlite")

        self.database_name = database_name
        self.method_name = method_name
        self.sample_id = sample_id
        self.test_id = test_id

        self.epoch_timestamp = datetime.now().timestamp()
        self.human_timestamp = datetime.now()

        if options.enable_asynchronous_payload_delivery:
            self.upload_payload_to_database_async()

        else:
            self.upload_payload_to_database_sync()

    def upload_payload_to_database_async(self):
        """
        Returns
        -------

        """
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_in_executor(executor=None, func=self.send_payload_to_database)

    def upload_payload_to_database_sync(self):
        """
        Returns
        -------

        """
        self.send_payload_to_database()

    def send_payload_to_database(self):
        """
        :return:
        """
        payload = []
        for row in self.iterate_through_profiled_stack():

            # Dividing payload into multiple inserts to work around server-less variable restrictions
            if self.using_server_less_database is True and len(payload) == 999:
                # Sending and nuking payload variable when exceeding SQLite's max amount of variables.
                self.insert_performance_statistics(payload=payload, database=self.database_name)
                payload = []

            payload.append(row)

        # Inserting full payload into server-based database or sending left-overs to sever-less database
        self.insert_performance_statistics(payload=payload, database=self.database_name)

    def iterate_through_profiled_stack(self):
        """

        :return:
        """
        try:
            for function, (cc, nc, tt, ct, callers) in self.performance_statistics.items():

                # will filter out the empty ends of the stack
                if len(callers) == 0:
                    continue

                child_path = function[0]
                child_line_number = function[1]
                child_function_name = function[2]

                for row in callers:
                        yield {
                            "test_id": self.test_id,
                            "sample_id": self.sample_id,
                            "test_case_name": self.database_name,
                            "name_of_method_under_test": self.method_name,
                            "epoch_timestamp": self.epoch_timestamp,
                            "human_timestamp": self.human_timestamp,
                            "child_path": child_path,
                            "child_line_number": child_line_number,
                            "child_function_name": child_function_name,
                            "parent_path": row[0],
                            "parent_line_number": row[1],
                            "parent_function_name": row[2],
                            "number_of_calls": nc,
                            "total_time": tt,
                            "cumulative_time": ct,
                            "total_response_time": self.total_response_time
                        }

        except Exception:
            raise AgentCannotProcessProfilerOutput()


class SystemResourcesInterpreter(Crud):

    def __init__(self, cpu_statistics, database_name, method_name, sample_id, test_id):
        super(SystemResourcesInterpreter, self).__init__()

        self.cpu_statistics = cpu_statistics
        self.database_name = database_name
        self.method_name = method_name
        self.sample_id = sample_id
        self.test_id = test_id

        if options.enable_asynchronous_payload_delivery:
            self.upload_payload_to_database_async()

        else:
            self.upload_payload_to_database_sync()

    def construct_payload(self):
        """

        Returns
        -------

        """
        payload = []
        meta_data = {"test_id": self.test_id, "test_case_name": self.database_name,
                     "sample_id": self.sample_id, "name_of_method_under_test": self.method_name}

        for measurements in self.cpu_statistics:
            payload.append({**meta_data, **measurements})

        return payload

    def upload_payload_to_database_async(self):
        """
        Returns
        -------

        """
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_in_executor(executor=None, func=self.send_payload)

    def upload_payload_to_database_sync(self):
        """
        Returns
        -------

        """
        self.send_payload()

    def send_payload(self):
        """
        :return:
        """
        payload = self.construct_payload()
        self.insert_system_resources_statistics(payload=payload, database=self.database_name)
