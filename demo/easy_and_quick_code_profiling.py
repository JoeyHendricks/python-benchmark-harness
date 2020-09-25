from demo.example_of_slow_and_fast_functions import *
from QuickPotato.configuration.manager import options  # <-- Import the options object
from QuickPotato.harness.export import TimeSpentStatisticsExport


options.enable_profiling = True  # <-- Set to True to enable profiling

fast_method()

options.enable_profiling = False  # <-- Set to False to disable profiling

# Export all results to csv
TimeSpentStatisticsExport(
    path="C:\\Temp\\",
    purge_database_after_export=True  # <-- Optionally clean-up the database after use.
).to_csv()
