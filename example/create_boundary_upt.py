from CouchPotato.profiling.intrusive import performance_test as pt
from CouchPotato.configuration.management import options
from CouchPotato.statistical.visualizations import CsvFile, FlameGraph
from example.example_code import FancyCode

pt.test_case_name = "test_performance"  # <-- Define test case name
pt.max_and_min_boundary_for_average = {"max": 1, "min": 0.001}  # <-- Establish performance boundaries

options.enable_intrusive_profiling = True  # <-- Set to True to enable profiling

# Execute method under test
for _ in range(0, 10):
    FancyCode().say_my_name_and_more(name="joey hendricks")

options.enable_intrusive_profiling = False  # <-- Set to False to disable profiling

# Analyse profiled results will output True if boundaries are not breached otherwise False
results = pt.verify_benchmark_against_set_boundaries

# Export time spent statistical to csv
CsvFile(test_case_name="test_performance", test_id=pt.current_test_id).export(path="C:\\temp\\")
FlameGraph(test_case_name="test_performance", test_id=pt.current_test_id).export(path="C:\\temp\\")
