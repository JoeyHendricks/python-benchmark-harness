from examples.example_code import FancyCode
from QuickPotato.profiling.intrusive import performance_test as pt
from QuickPotato.configuration.management import options
from QuickPotato.statistical.visualizations import FlameGraph, HeatMap

options.enable_intrusive_profiling = True  # <-- Make sure that profiling is enabled

# Create a test case
pt.test_case_name = "exploratory performance test"

# Execute your code in the way you want.
for i in range(0, 10):
    FancyCode().say_my_name_and_more(
        name="joey hendricks")  # <-- Make sure the performance breakpoint is added (the decorator).

# Generate visualizations to analyse your code.
FlameGraph(test_case_name=pt.test_case_name, test_id=pt.current_test_id).export("C:\\temp\\")
HeatMap(test_case_name=pt.test_case_name, test_ids=[pt.current_test_id]).export("C:\\temp\\")
