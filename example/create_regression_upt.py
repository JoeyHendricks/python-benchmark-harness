from CouchPotato.profiling.intrusive import performance_test as pt
from CouchPotato.configuration.management import options
from CouchPotato.statistical.visualizations import CsvFile, FlameGraph
from example.example_code import fast_method


pt.test_case_name = "test_performance"  # <-- Define test case name

options.enable_intrusive_profiling = True  # <-- Set to True to enable profiling

# Execute method under test
for _ in range(0, 10):
    fast_method()

options.enable_intrusive_profiling = False  # <-- Set to False to disable profiling

# Analyse results for change True if there is no change otherwise False
results = pt.verify_benchmark_against_previous_baseline

# Export visualizations
CsvFile(test_case_name="test_performance", test_id=pt.current_test_id).export(path="C:\\temp\\")
FlameGraph(test_case_name="test_performance", test_id=pt.current_test_id).export(path="C:\\temp\\")
