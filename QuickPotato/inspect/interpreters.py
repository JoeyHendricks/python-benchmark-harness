from QuickPotato.database.actions import DatabaseActions
from QuickPotato.utilities.exceptions import *
from QuickPotato.configuration.options import asynchronous_payload_delivery
from datetime import datetime
import asyncio
import re


class TimeSpentInterpreter(DatabaseActions):

    def __init__(self, time_spent_metrics, database_name, method_name, method_id, test_id):
        super(TimeSpentInterpreter, self).__init__()

        self.time_spent_metrics = time_spent_metrics
        self.response_times = self.extract_response_time()

        self.database_name = database_name
        self.method_name = method_name
        self.method_id = method_id
        self.test_id = test_id

        self.epoch_timestamp = datetime.now().timestamp()
        self.human_timestamp = datetime.now()

        if asynchronous_payload_delivery:
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
        self.insert_time_spent_statistics(payload=payload, database_name=self.database_name)

    def construct_payload(self):
        """
        :return:
        """
        try:
            # Generate a dictionary
            stack = []
            header = ['number_of_calls', 'total_time', 'total_time_per_call',
                      'cumulative_time', 'cumulative_time_per_call', 'file', 'line_number', 'function_name']

            meta_data = {"test_id": self.test_id, "uuid": self.method_id, "test_case_name": self.database_name,
                         "name_of_method_under_test": self.method_name, "response_time": self.response_times,
                         "epoch_datetime": self.epoch_timestamp, "human_datetime": self.human_timestamp}

            for line in self.convert_payload_to_dictionary(header=header, meta=meta_data):
                stack.append(line)

            return stack

        except Exception:
            raise AgentCannotProcessProfilerOutput()

    def convert_payload_to_dictionary(self, header, meta):
        """
        :return:
        """
        # Dump performance statistics from the buffer to local variables
        buffer = 'ncalls' + self.time_spent_metrics.split('ncalls')[-1]
        buffer = '\n'.join([','.join(line.rstrip().split(None, 5)) for line in buffer.split('\n')])
        buffer = list(filter(None, buffer.split('\n')))

        for count, line in enumerate(buffer, 1):
            if count == 1:
                continue

            elif count == len(buffer):
                continue

            else:
                line = line.split(",")

                # Forcing the last value containing the file path,
                # line number and method name to be split in three
                tail = line[-1]
                del line[-1]

                # Checking if method is a Python builtin method
                if "{" in tail or "}" in tail:
                    line.append("None")  # File Name
                    line.append("0")     # Line Number
                    line.append(tail)    # Method Name

                else:
                    line.append(str(tail.split(".py:")[0] + ".py"))                            # File Path
                    line.append(str(re.search(r'(?:>:|.py:)(.*?)\(', str(tail)).group(1)))     # Line Number
                    line.append(str(tail.split("(")[1]).strip("()"))                           # Method Name

                yield self.convert_dictionary_values_to_correct_data_type(payload={**meta, **dict(zip(header, line))})

    @staticmethod
    def convert_dictionary_values_to_correct_data_type(payload):
        """
        :param payload:
        :return:
        """
        payload["total_time"] = float(payload["total_time"])
        payload["total_time_per_call"] = float(payload["total_time_per_call"])
        payload["cumulative_time"] = float(payload["cumulative_time"])
        payload["cumulative_time_per_call"] = float(payload["cumulative_time_per_call"])
        payload["line_number"] = int(payload["line_number"])

        return payload

    def extract_response_time(self):
        """
        :return:
        """
        return float(re.search(r' in (.*?) seconds', str(self.time_spent_metrics)).group(1))


class SystemResourcesInterpreter(DatabaseActions):

    def __init__(self, cpu_metrics, database_name, method_name, method_id, test_id):
        super(SystemResourcesInterpreter, self).__init__()

        self.measurements_of_process_cpu_usage = cpu_metrics["measurements_of_process_cpu_usage"]
        self.measurements_of_system_cpu_usage = cpu_metrics["measurements_of_system_cpu_usage"]

        self.database_name = database_name
        self.method_name = method_name
        self.method_id = method_id
        self.test_id = test_id

        self.epoch_timestamp = datetime.now().timestamp()
        self.human_timestamp = datetime.now()

        if asynchronous_payload_delivery:
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
                     "uuid": self.method_id, "name_of_method_under_test": self.method_name,
                     "epoch_datetime": self.epoch_timestamp, "human_datetime": self.human_timestamp}

        for process_cpu_usage, system_cpu_usage in zip(self.measurements_of_process_cpu_usage,
                                                       self.measurements_of_system_cpu_usage):

            cpu_metrics = {"percentage_of_process_cpu_usage": process_cpu_usage,
                           "percentage_of_system_cpu_usage": system_cpu_usage}

            payload.append({**meta_data, **cpu_metrics})

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
        self.insert_system_resources_statistics(payload=payload, database_name=self.database_name)
