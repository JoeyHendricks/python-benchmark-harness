from .._database.collection import Crud
from .._configuration import options
from datetime import datetime
from uuid import uuid4
import asyncio


class ProfilerStatisticsInterpreter(Crud):

    def __init__(self, test_case_name, connection_url, performance_statistics,
                 total_response_time, method_name, sample_id, test_id):

        super(ProfilerStatisticsInterpreter, self).__init__()

        self.performance_statistics = performance_statistics
        self.total_response_time = total_response_time
        self._connection_url = connection_url

        self.test_case_name = test_case_name
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
            if self._connection_url[0:6] == "sqlite" and len(payload) == 10:
                # Sending and nuking payload variable when exceeding SQLite's max amount of variables.
                self.bulk_insert(
                    connection_url=self._connection_url,
                    table=self.c_profiler_statistics_data_model(self.test_case_name),
                    payload=payload
                )
                payload = []
            payload.append(row)

        # Inserting full payload into server-based _database or sending the left-overs to sever-less _database
        self.bulk_insert(
            connection_url=self._connection_url,
            table=self.c_profiler_statistics_data_model(self.test_case_name),
            payload=payload
        )

    def iterate_through_profiled_stack(self):
        """

        :return:
        """
        for function, (cc, nc, tt, ct, callers) in self.performance_statistics.items():

            child_path = function[0]
            child_line_number = function[1]
            child_function_name = function[2]

            if len(callers) == 0 and str(function[2]) == self.method_name:
                yield {
                    "uuid": str(uuid4()),
                    "test_id": self.test_id,
                    "sample_id": self.sample_id,
                    "test_case_name": self.test_case_name,
                    "name_of_method_under_test": self.method_name,
                    "epoch_timestamp": self.epoch_timestamp,
                    "human_timestamp": self.human_timestamp,
                    "child_path": child_path,
                    "child_line_number": child_line_number,
                    "child_function_name": child_function_name,
                    "parent_path": "~",
                    "parent_line_number": 0,
                    "parent_function_name": self.sample_id,
                    "number_of_calls": nc,
                    "total_time": tt,
                    "cumulative_time": ct,
                    "total_response_time": self.total_response_time
                }

            elif len(callers) == 0:
                continue

            else:
                for row in callers:
                    yield {
                        "uuid": str(uuid4()),
                        "test_id": self.test_id,
                        "sample_id": self.sample_id,
                        "test_case_name": self.test_case_name,
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
