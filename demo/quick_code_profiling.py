from demo.example_code import *
from QuickPotato.configuration.manager import options  # <-- Import the options object
from QuickPotato.harness.export import TimeSpentStatisticsExport


options.enable_intrusive_profiling = True  # <-- Set to True to enable profiling

fast_method()

options.enable_intrusive_profiling = False  # <-- Set to False to disable profiling

# Export all results to csv
TimeSpentStatisticsExport(
    path="C:\\Temp\\",
    purge_database_after_export=True  # <-- Optionally clean-up the database after use.
).to_csv()
