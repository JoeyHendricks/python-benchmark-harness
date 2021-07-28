from examples.non_intrusive_example_code import FancyCode
from QuickPotato import performance_test as pt
from QuickPotato.statistical.visualizations import FlameGraph, HeatMap, CsvFile, BarChart

# Create a test case
pt.database_name = "test case A"
pt.test_case_name = "exploratory performance test"

# Attach the method from which you want to performance test
pt.measure_method_performance(
    method=FancyCode().say_my_name_and_more,  # <-- The Method which you want to test.
    arguments=["joey hendricks"],  # <-- Your arguments go here.
    iteration=1,  # <-- The number of times you want to execute this method.
    pacing=0,  # <-- How much seconds you want to wait between iterations.
)

# Generate visualizations to analyse your code.
barchart = BarChart(
    test_case_name=pt.test_case_name,
    database_name=pt.database_name,
    test_ids=[pt.current_test_id, pt.previous_test_id]
)
flamegraph = FlameGraph(
    test_case_name=pt.test_case_name,
    database_name=pt.database_name,
    test_id=pt.current_test_id
)
heatmap = HeatMap(
    test_case_name=pt.test_case_name,
    database_name=pt.database_name,
    test_ids=[pt.current_test_id, pt.previous_test_id]
)
csv = CsvFile(
    test_case_name=pt.test_case_name,
    database_name=pt.database_name,
    test_id=pt.current_test_id
)

for chart in [barchart, flamegraph, heatmap, csv]:
    chart.export("C:\\temp\\")
