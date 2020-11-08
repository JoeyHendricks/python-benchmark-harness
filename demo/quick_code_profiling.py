from demo.example_code import *
from QuickPotato.configuration.management import options  # <-- Import the options object
from QuickPotato.harness.export import PerformanceStatisticsExport


options.enable_intrusive_profiling = True  # <-- Set to True to enable profiling

fast_method()

options.enable_intrusive_profiling = False  # <-- Set to False to disable profiling

# Export all results to csv
PerformanceStatisticsExport(
    path="C:\\Temp\\",
    purge_database_after_export=True  # <-- Optionally clean-up the database after use.
).to_csv()
