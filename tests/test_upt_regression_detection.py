from QuickPotato.inspect.intrusive import unit_performance_test as upt
from QuickPotato.database.management import DatabaseManager
from QuickPotato.configuration.management import options
from demo.example_code import *
import unittest

SAMPLE_SIZE = 10
UNIT_TEST_DATABASE_NAME = "upt_unit_tests_regression_detection_with_t_test"


class TestRegressionDetectionTTest(unittest.TestCase):

    def setUp(self):
        """

        """
        options.enable_intrusive_profiling = True

    def tearDown(self):
        """

        """
        options.enable_intrusive_profiling = False

    @staticmethod
    def clean_up_database():
        """

        """
        database_manager = DatabaseManager()
        database_manager.delete_result_database(UNIT_TEST_DATABASE_NAME)

    @staticmethod
    def create_baseline(slow_baseline=False, fast_baseline=False):
        """

        """
        # Defining test case
        upt.test_case_name = UNIT_TEST_DATABASE_NAME
        upt.silence_warning_messages = True

        # Execute statistical test
        upt.run_t_test = True
        upt.silence_warning_messages = True

        # Run baseline test
        for _ in range(0, SAMPLE_SIZE):
            if slow_baseline and fast_baseline is False:
                slow_method()
            else:
                fast_method()

        # Analyse test results
        results = upt.verify_benchmark_against_previous_baseline

        # printing information message about baseline
        print("------------------------------BASELINE------------------------------")
        print(f"Previous test id :{upt.previous_test_id}")
        print(f"Current  test id :{upt.current_test_id}")
        if slow_baseline and fast_baseline is False:
            print(f"Slow baseline has been established first run status: {results}")
        else:
            print(f"Fast baseline has been established first run status: {results}")

        print(f"Raw Response Times: {upt.benchmark_measurements.response_times()}")
        print(f"Average Response Time: {upt.benchmark_measurements.average_response_time()}")

        return results

    def test_regression_slower_benchmark(self):
        """

        """
        # Establishing slow baseline and cleaning up database
        self.clean_up_database()
        self.create_baseline(fast_baseline=True)

        # Defining test case
        upt.test_case_name = UNIT_TEST_DATABASE_NAME
        upt.run_t_test = True

        for _ in range(0, SAMPLE_SIZE):
            slow_method()

        # Analyse test results
        results = upt.verify_benchmark_against_previous_baseline
        
        # Print Details of this test
        print("------------------------------BENCHMARK-----------------------------")
        print(f"Benchmark test results: {results}")
        print(f"Raw Response Times: {upt.benchmark_measurements.response_times()}")
        print(f"Average Response Time: {upt.benchmark_measurements.average_response_time()}")
        print("--------------------------------------------------------------------")

        # Expected results is a failure because the test changed
        self.assertFalse(results)

    def test_regression_faster_benchmark(self):
        """

        """
        # Establishing slow baseline
        self.clean_up_database()
        self.create_baseline(slow_baseline=True)

        # Defining test case
        upt.test_case_name = UNIT_TEST_DATABASE_NAME
        upt.run_t_test = True

        for _ in range(0, SAMPLE_SIZE):
            fast_method()

        # Analyse test results
        results = upt.verify_benchmark_against_previous_baseline

        # Print Details of this test
        print("------------------------------BENCHMARK-----------------------------")
        print(f"Benchmark test results: {results}")
        print(f"Raw Response Times: {upt.benchmark_measurements.response_times()}")
        print(f"Average Response Time: {upt.benchmark_measurements.average_response_time()}")
        print("--------------------------------------------------------------------")

        # Expected results is a failure because the test changed
        self.assertFalse(results)

    def test_regression_no_change(self):
        """

        """
        # Establishing slow baseline
        self.clean_up_database()
        self.create_baseline(fast_baseline=True)

        # Defining test case
        upt.test_case_name = UNIT_TEST_DATABASE_NAME
        upt.run_t_test = True

        for _ in range(0, SAMPLE_SIZE):
            fast_method()

        # Analyse test results
        results = upt.verify_benchmark_against_previous_baseline

        # Print Details of this test
        print("------------------------------BENCHMARK-----------------------------")
        print(f"Benchmark test results: {results}")
        print(f"Raw Response Times: {upt.benchmark_measurements.response_times()}")
        print(f"Average Response Time: {upt.benchmark_measurements.average_response_time()}")
        print("--------------------------------------------------------------------")

        # Expected results is a failure because the test changed
        self.assertTrue(results)

    def test_regression_fail_than_pass(self):
        """

        """
        # Establishing fast baseline
        self.clean_up_database()
        self.create_baseline(fast_baseline=True)

        def test_1_slower_code():

            # ----------- Test 1 slower code -----------

            # Defining test case
            upt.test_case_name = UNIT_TEST_DATABASE_NAME
            upt.run_t_test = True

            # Run your code
            for _ in range(0, SAMPLE_SIZE):
                slow_method()  # <--- SLOWER

            # Analyse test results
            results = upt.verify_benchmark_against_previous_baseline

            # Expected results is a failure because the test changed
            print("------------------------------BENCHMARK 1 -----------------------------")
            print(f"Previous test id :{upt.previous_test_id}")
            print(f"Current  test id :{upt.current_test_id}")
            print(f"Benchmark test results: {results}")
            print(f"Raw Response Times: {upt.benchmark_measurements.response_times()}")
            print(f"Average Response Time: {upt.benchmark_measurements.average_response_time()}")
            print("----------------------------------------------------------------------")

            return results

        def test_2_same_code():
            # ------------ Test 2 same code ------------

            # Defining test case
            upt.test_case_name = UNIT_TEST_DATABASE_NAME
            upt.run_t_test = True

            # Run your code
            for _ in range(0, SAMPLE_SIZE):
                fast_method()  # <--- FASTER

            # Analyse test results
            results = upt.verify_benchmark_against_previous_baseline

            # Expected results is a failure because the test changed
            print("------------------------------BENCHMARK 2 -----------------------------")
            print(f"Previous test id :{upt.previous_test_id}")
            print(f"Current  test id :{upt.current_test_id}")
            print(f"Benchmark test results: {results}")
            print(f"Raw Response Times: {upt.benchmark_measurements.response_times()}")
            print(f"Average Response Time: {upt.benchmark_measurements.average_response_time()}")
            print("----------------------------------------------------------------------")
            return results

            # ------------------------------------------

        self.assertFalse(test_1_slower_code())
        self.assertTrue(test_2_same_code())

    def test_statistical_accuracy(self):
        """

        """
        self.create_baseline(fast_baseline=True)

        results = []

        for _ in range(0, 10000):

            # Define Test Case
            upt.test_case_name = UNIT_TEST_DATABASE_NAME
            upt.run_t_test = True

            # Execute method under test
            for _ in range(0, SAMPLE_SIZE):
                fast_method()

            # Analyse results
            output = upt.verify_benchmark_against_previous_baseline
            results.append(output)

        print(f"passed: {results.count(True)} failed: {results.count(False)} total: 100")

        percentage = (results.count(True) - len(results)) / results.count(True) * 100
        self.assertLess(percentage, 5)
