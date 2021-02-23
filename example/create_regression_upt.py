from CouchPotato.profiling.intrusive import unit_performance_test as upt
from CouchPotato.configuration.management import options
from CouchPotato.harness.export import PerformanceStatisticsExport
from example.example_code import fast_method


upt.test_case_name = "test_performance"  # <-- Define test case name

options.enable_intrusive_profiling = True  # <-- Set to True to enable profiling

# Execute method under test
for _ in range(0, 10):
    fast_method()

options.enable_intrusive_profiling = False  # <-- Set to False to disable profiling

# Analyse results for change True if there is no change otherwise False
results = upt.verify_benchmark_against_previous_baseline

# Export time spent statistical to csv
if results is False:
    PerformanceStatisticsExport(
        test_case_name=upt.test_case_name,
        test_id=upt.current_test_id,
        delimiter=";",
        path="C:\\Temp\\"
    ).to_csv()
