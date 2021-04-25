from example.example_code import FancyCode, slow_method, fast_method
from QuickPotato.profiling.intrusive import performance_test as pt
from QuickPotato.configuration.management import options
from QuickPotato.statistical.visualizations import FlameGraph, HeatMap

options.enable_intrusive_profiling = True  # <-- Make sure that profiling is enabled
options.allow_the_selection_of_untested_or_failed_test_ids = True  # <-- Used to also be able to select failed test

pt.test_case_name = "exploratory performance test"
test_data = ["joey", "joey hendricks"]

for i in range(0, 100):
    FancyCode().say_my_name_and_more(name=test_data[1])

HeatMap(test_case_name=pt.test_case_name, test_ids=[pt.previous_test_id, pt.current_test_id]).export("C:\\temp\\")
FlameGraph(test_case_name=pt.test_case_name, test_id=pt.current_test_id).export("C:\\temp\\")

options.allow_the_selection_of_untested_or_failed_test_ids = False
