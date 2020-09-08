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

        self.measurements_of_process_cpu_usage = []
        self.measurements_of_system_cpu_usage = []

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
            self.measurements_of_process_cpu_usage.append(self.HOST_PROCESS.cpu_percent() / psutil.cpu_count())
            self.measurements_of_system_cpu_usage.append(psutil.cpu_percent())

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
        function_output = method(*args, **kwargs)
        timer.disable()
        self.disable_collection_of_system_resource_utilization()

        # Dump performance statistics from the buffer to local variables
        profiler_output = io.StringIO()
        ps = pstats.Stats(timer, stream=profiler_output)
        ps.sort_stats('cumulative').print_stats()
        profiler_output = profiler_output.getvalue()

        return {"functional_output": function_output,
                "time_spent_metrics": profiler_output,
                "cpu_metrics": {"measurements_of_process_cpu_usage": self.measurements_of_process_cpu_usage,
                                "measurements_of_system_cpu_usage": self.measurements_of_system_cpu_usage}
                }
