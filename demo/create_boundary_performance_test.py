from QuickPotato.inspect.intrusive import unit_performance_test as upt
from QuickPotato.configuration.manager import options
from QuickPotato.harness.export import export_all_time_spent_statistics_to_csv
from demo.example_of_slow_and_fast_functions import fast_method

upt.test_case_name = "verify_performance_of_fast_method"  # <-- Define test case name
upt.max_and_min_boundary_for_average = {"max": 1, "min": 0.001}  # <-- Establish performance boundaries

options.enable_profiling = True  # <-- Set to True to enable profiling

# Execute method under test
for _ in range(0, 10):
    fast_method()

# Analyse profiled results will output True if boundaries are not breached otherwise False
results = upt.verify_if_benchmark_does_not_breach_defined_boundaries()

options.enable_profiling = False  # <-- Set to False to disable profiling

# Export time spent statistics to csv
export_all_time_spent_statistics_to_csv(
    test_case_name=upt.test_case_name,
    test_id=upt.current_test_id,
    delimiter=";",
    path="C:\\Temp\\"
)
