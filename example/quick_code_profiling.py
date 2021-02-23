from example.example_code import FancyCode
from CouchPotato.configuration.management import options
from CouchPotato.statistical.visualizations import FlameGraph


options.enable_intrusive_profiling = True  # <-- Make sure that profiling is enabled

FancyCode().say_my_name_and_more(name="joey hendricks")

# Generate Flame Graph
FlameGraph().export("C:\\temp\\")
