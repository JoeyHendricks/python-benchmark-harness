from examples.non_intrusive_example_code import FancyCode
from QuickPotato import micro_benchmark as pt
from QuickPotato.visualizations.visualizations import FlameGraph, HeatMap, BarChart
from visuals import LineGraph
import pandas as pd

# Create a test case
pt.test_case_name = "demo"

# Attach the method from which you want to performance test
pt.measure_method_performance(
    method=FancyCode().say_my_name_and_more,  # <-- The Method which you want to test.
    arguments=["x"],  # <-- Your arguments go here.
    iteration=20,  # <-- The number of times you want to execute this method.
    pacing=0,  # <-- How much seconds you want to wait between iterations.
)
print(f"{pt.current_test_id}-{pt.previous_test_id}")
print(pt.benchmark_statistics.raw_data)
print(pt.baseline_statistics.raw_data)
print(len(pt.benchmark_statistics.raw_data))
print(len(pt.baseline_statistics.raw_data))
print("-------")
print(pt.compare_benchmark(minimum_score=90, minimum_letter_rank="A"))
print(pt.distance_test_statistics.wasserstein_distance)
print(pt.distance_test_statistics.kolmogorov_smirnov_distance)
print(pt.score)
print(pt.rank)

LineGraph(
    benchmark=pt.distance_test_statistics.sample_a,
    baseline=pt.distance_test_statistics.sample_b,
    kolmogorov_smirnov_distance=pt.distance_test_statistics.kolmogorov_smirnov_distance,
    wasserstein_distance=pt.distance_test_statistics.wasserstein_distance,
    rank=pt.rank,
    score=pt.score,
    change=0
).show()

exit()
# vorige benchmark
FlameGraph(
    test_case_name=pt.test_case_name,
    test_id=pt.previous_test_id,
    database_connection_url=pt.database_connection_url
)

# current benchmark
FlameGraph(
    test_case_name=pt.test_case_name,
    test_id=pt.current_test_id,
    database_connection_url=pt.database_connection_url
)

"""
# Generate visualizations to analyse your code.
barchart = BarChart(
    test_case_name=pt.test_case_name,
    database_name=pt.database_connection_url,
    test_ids=[pt.current_test_id, pt.previous_test_id]
)
flamegraph = FlameGraph(
    test_case_name=pt.test_case_name,
    database_name=pt.database_connection_url,
    test_id=pt.current_test_id
)
heatmap = HeatMap(
    test_case_name=pt.test_case_name,
    database_name=pt.database_connection_url,
    test_ids=[pt.current_test_id, pt.previous_test_id]
)
csv = CsvFile(
    test_case_name=pt.test_case_name,
    database_name=pt.database_connection_url,
    test_id=pt.current_test_id
)

for chart in [barchart, flamegraph, heatmap, csv]:
    chart.export("C:\\temp\\")
"""