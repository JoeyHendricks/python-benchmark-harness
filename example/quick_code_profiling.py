from example.example_code import FancyCode
from QuickPotato.configuration.management import options
from QuickPotato.analysis.analysis import FlameGraphs


options.enable_intrusive_profiling = True  # <-- Make sure that profiling is enabled

FancyCode().say_my_name_and_more(name="joey hendricks")

# Generate Flame Graph
FlameGraphs().export_flame_graph(path="C:\\temp\\")
