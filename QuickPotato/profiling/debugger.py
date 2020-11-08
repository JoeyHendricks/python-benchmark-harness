from QuickPotato.configuration.management import options
from datetime import datetime
from time import time
import threading
import cProfile
import pstats
import psutil


class Profiler(object):

    HOST_PROCESS = psutil.Process()

    def __init__(self):

        self.collection_system_resource_utilization = False
        self.system_resource_utilization_measurements = []
        self.functional_output = None
        self.total_response_time = None
        self.performance_statistics = None

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
        # Initializing the Profiler, ProfileResults and creating the results
        profiler = cProfile.Profile()

        # Start Profiling the method
        start_time = time()
        self.enable_collection_of_system_resource_utilization()
        profiler.enable()
        self.functional_output = method(*args, **kwargs)
        profiler.disable()
        self.disable_collection_of_system_resource_utilization()
        end_time = time()
        self.total_response_time = end_time - start_time

        # Dump performance statistical
        self.performance_statistics = pstats.Stats(profiler).stats
