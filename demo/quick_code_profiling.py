from demo.example_code import *
from QuickPotato.configuration.management import options  # <-- Import the options object
from QuickPotato.harness.analysis import FlameGraphs


options.enable_intrusive_profiling = True  # <-- Make sure that profiling is enabled

fast_method()

# Generate Flame Graph
FlameGraphs().export_flame_graph(path="C:\\Temp\\")
