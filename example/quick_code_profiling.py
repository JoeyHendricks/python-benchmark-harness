from example.example_code import FancyCode, slow_method, fast_method
from QuickPotato.profiling.intrusive import performance_test as pt
from QuickPotato.configuration.management import options
from QuickPotato.statistical.visualizations import FlameGraph, CsvFile, HeatMap


options.enable_intrusive_profiling = True  # <-- Make sure that profiling is enabled
pt.test_case_name = "exploratory performance test"
test_data = ["joey", "joey hendricks"]

for i in range(0, 4):
    #fast_method()
    FancyCode().say_my_name_and_more(name=test_data[1])

heatmap = HeatMap(test_case_name=pt.test_case_name, test_id=pt.current_test_id)
print(heatmap.code_paths)  # <-- playing with this :)
exit()

FlameGraph().export("C:\\temp\\")
CsvFile().export("C:\\temp\\")

