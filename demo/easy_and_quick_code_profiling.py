from demo.example_of_slow_and_fast_functions import *
from QuickPotato.configuration.manager import options  # Import the options object


options.enable_profiling = True  # <-- Set to True to enable profiling

fast_method()

options.enable_profiling = False  # <-- Set to False to disable profiling
