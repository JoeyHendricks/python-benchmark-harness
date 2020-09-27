from QuickPotato.inspect.intrusive import unit_performance_test as upt
from QuickPotato.configuration.manager import options
from QuickPotato.harness.export import TimeSpentStatisticsExport
from demo.example_code import fast_method


upt.test_case_name = "test_performance"  # <-- Define test case name
upt.regression_setting_perform_f_test = True  # <-- Turn on f-test
upt.regression_setting_perform_t_test = True  # <-- Turn on t-test

options.enable_intrusive_profiling = True  # <-- Set to True to enable profiling

# Execute method under test
for _ in range(0, 10):
    fast_method()

options.enable_intrusive_profiling = False  # <-- Set to False to disable profiling

# Analyse results for change True if there is no change otherwise False
results = upt.verify_that_there_is_no_change_between_the_baseline_and_benchmark()

# Export time spent statistics to csv
if results is False:
    TimeSpentStatisticsExport(
        test_case_name=upt.test_case_name,
        test_id=upt.current_test_id,
        delimiter=";",
        path="C:\\Temp\\"
    ).to_csv()
