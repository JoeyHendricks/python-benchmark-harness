from datetime import datetime
import threading
import cProfile
import pstats
import psutil
import io


class Profiler:

    HOST_PROCESS = psutil.Process()

    def __init__(self):

        self.measure_cpu = False
        self.measure_mem = False

        self.functional_output = None
        self.time_spent_statistics = None
        self.cpu_measurements = []

    def enable_collection_of_system_resource_utilization(self):
        """

        Returns
        -------

        """
        cpu_measure_thread = threading.Thread(target=self.measure_cpu_usage)
        # mem_measure_thread = threading.Thread(target=self.run)

        self.measure_cpu = True
        # self.measure_mem = True

        cpu_measure_thread.start()
        # mem_measure_thread.start()

        return True

    def disable_collection_of_system_resource_utilization(self):
        """

        Parameters
        ----------

        Returns
        -------

        """
        self.measure_cpu = False
        self.measure_mem = False

        return True

    def measure_cpu_usage(self):
        """

        Returns
        -------

        """
        while self.measure_cpu:
            row = {
                "epoch_timestamp": datetime.now().timestamp(),
                "human_timestamp": datetime.now(),
                "percentage_of_system_cpu_usage": psutil.cpu_percent(),
                "percentage_of_process_cpu_usage": self.HOST_PROCESS.cpu_percent() / psutil.cpu_count()
             }
            self.cpu_measurements.append(row)

    def measure_mem_usage(self):
        pass

    def profile_method_under_test(self, method, *args, **kwargs):
        """

        Returns
        -------

        """
        # Initializing the Profiler, ProfileResults and creating the buffer
        timer = cProfile.Profile()

        # Start Profiling the method
        self.enable_collection_of_system_resource_utilization()
        timer.enable()
        self.functional_output = method(*args, **kwargs)
        timer.disable()
        self.disable_collection_of_system_resource_utilization()

        # Dump performance statistics from the buffer to local variables
        self.time_spent_statistics = io.StringIO()
        ps = pstats.Stats(timer, stream=self.time_spent_statistics)
        ps.sort_stats('cumulative').print_stats()
        self.time_spent_statistics = self.time_spent_statistics.getvalue()

        return True
