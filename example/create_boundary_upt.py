from QuickPotato.profiling.intrusive import unit_performance_test as upt
from QuickPotato.configuration.management import options
from QuickPotato.harness.export import PerformanceStatisticsExport
from example.example_code import fast_method

upt.test_case_name = "test_performance"  # <-- Define test case name
upt.max_and_min_boundary_for_average = {"max": 1, "min": 0.001}  # <-- Establish performance boundaries

options.enable_intrusive_profiling = True  # <-- Set to True to enable profiling

# Execute method under test
for _ in range(0, 10):
    fast_method()

options.enable_intrusive_profiling = False  # <-- Set to False to disable profiling

# Analyse profiled results will output True if boundaries are not breached otherwise False
results = upt.verify_benchmark_against_set_boundaries

# Export time spent statistical to csv
if results is False:
    PerformanceStatisticsExport(
        test_case_name=upt.test_case_name,
        test_id=upt.current_test_id,
        delimiter=";",
        path="C:\\Temp\\",
        purge_database_after_export=True  # <-- Optionally clean-up the database after use.
    ).to_csv()
