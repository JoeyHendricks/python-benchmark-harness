from examples.example_code import FancyCode
from QuickPotato.profiling.intrusive import performance_test as pt
from QuickPotato.statistical.visualizations import FlameGraph, HeatMap, CsvFile, BarChart

# Create a test case
pt.test_case_name = "exploratory performance test"

# Attach the method from which you want to performance test
pt.measure_method_performance(
    method=FancyCode().say_my_name_and_more,  # <-- The Method which you want to test.
    arguments=["joey hendricks"],  # <-- Your arguments go here.
    iteration=10,  # <-- The number of times you want to execute this method.
    pacing=0  # <-- How much seconds you want to wait between iterations.
)

# Generate visualizations to analyse your code.
BarChart(test_case_name=pt.test_case_name, test_ids=[pt.current_test_id, pt.previous_test_id]).export("C:\\temp\\")
FlameGraph(test_case_name=pt.test_case_name, test_id=pt.current_test_id).export("C:\\temp\\")
HeatMap(test_case_name=pt.test_case_name, test_ids=[pt.current_test_id, pt.previous_test_id]).export("C:\\temp\\")
CsvFile(test_case_name=pt.test_case_name, test_id=pt.current_test_id).export("C:\\temp\\")
