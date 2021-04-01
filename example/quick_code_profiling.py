from example.example_code import FancyCode, slow_method, fast_method
from QuickPotato.configuration.management import options
from QuickPotato.statistical.visualizations import FlameGraph, CsvFile, HeatMap


options.enable_intrusive_profiling = True  # <-- Make sure that profiling is enabled

fast_method()


HeatMap()
exit()

FlameGraph().export("C:\\temp\\")
CsvFile().export("C:\\temp\\")
