from example.example_code import FancyCode
from QuickPotato.profiling.intrusive import performance_test as pt
from QuickPotato.configuration.management import options
from QuickPotato.statistical.visualizations import FlameGraph, HeatMap

options.enable_intrusive_profiling = True  # <-- Make sure that profiling is enabled

pt.test_case_name = "exploratory performance test"

for i in range(0, 100):
    FancyCode().say_my_name_and_more(name="joey hendricks")

FlameGraph(test_case_name=pt.test_case_name, test_id=pt.current_test_id).export("C:\\temp\\")
HeatMap(test_case_name=pt.test_case_name, test_ids=[pt.current_test_id]).export("C:\\temp\\")
