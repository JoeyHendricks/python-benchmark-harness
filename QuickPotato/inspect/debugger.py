from QuickPotato.configuration.management import options
from datetime import datetime
import threading
import cProfile
import pstats
import psutil
import io


class Profiler:

    HOST_PROCESS = psutil.Process()

    def __init__(self):

        self.collection_system_resource_utilization = False
        self.system_resource_utilization_measurements = []
        self.functional_output = None
        self.time_spent_statistics = None

    def enable_collection_of_system_resource_utilization(self):
        """

        Returns
        -------

        """
        if options.enable_system_resource_collection:
            cpu_measure_thread = threading.Thread(target=self.measure_system_resource_utilization)
            self.collection_system_resource_utilization = True
            cpu_measure_thread.start()

    def disable_collection_of_system_resource_utilization(self):
        """

        Parameters
        ----------

        Returns
        -------

        """
        if options.enable_system_resource_collection:
            self.collection_system_resource_utilization = False

    def measure_system_resource_utilization(self):
        """

        Returns
        -------

        """
        while self.collection_system_resource_utilization:
            row = {
                "epoch_timestamp": datetime.now().timestamp(),
                "human_timestamp": datetime.now(),
                "percentage_of_system_cpu_usage": psutil.cpu_percent(),
                "percentage_of_process_cpu_usage": self.HOST_PROCESS.cpu_percent() / psutil.cpu_count()
             }
            self.system_resource_utilization_measurements.append(row)

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
