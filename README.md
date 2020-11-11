[![Couch Potato code in a lazy chair](/images/banner-with-text.jpg "Slow Potato Code")](https://github.com/JoeyHendricks/python-unit-level-performance-testing/blob/master/images/banner-with-text.jpg?raw=true)
---

QuickPotato is a unit-level performance testing framework for the Python programming language. 
It enables its users to define helpful test cases which can help catch problematic performance bottlenecks 
in the early stages of the development life cycle.

## How it works

### Installation

Install using [pip](https://pip.pypa.io/en/stable/) or download the source code from GitHub.
```bash
pip install QuickPotato
```
> Do note that QuickPotato hasn't released (yet) on the Python Package Index
> you can find a wheel file under the releases to install it. 

### Intrusive Testing

Using QuickPotato's intrusive performance testing method requires you to decorate your function. 
By tagging your function with the "performance_critical" decorator, you are providing QuickPotato access to profile
your code from that point once that functions exits the profiler will stop running.

This method allows you to pick and choose which methods you wish to profile.  
The "performance_critical" decorator also serves a human purpose by highlighting function 
that are critical to your codes performance.
 
This will remind you and your teammates to think about the performance of your code 
and include performance into your teams way of working.
An simple example of tagging your function with can be found below:

```python
from QuickPotato.profiling.intrusive import performance_critical  # <-- Import the decorator
import math


@performance_critical  # <-- Attach the decorator
def slow_method():
    num = 6 ** 6 ** 6
    return len(str(num))


@performance_critical  # <-- Attach the decorator
def fast_method():
    num = 6 ** 6 ** 6
    return int(math.log10(num))
```

### Quick Profiling 

Quickly gaining insights into the performance of your code is relatively easy with QuickPotato.  
Once you have imported and attached the "performance_critical" decorator to your function that you wish to profile.

With that achieved you are just a few lines of code away from pulling out detailed information about your code.
The code snippet below, shows you the basics you need to know to get the performance information out of your code: 

```python
from demo.example_code import FancyCode
from QuickPotato.configuration.management import options
from QuickPotato.harness.analysis import FlameGraphs


options.enable_intrusive_profiling = True  # <-- Make sure that profiling is enabled

# Your fancy code :)
FancyCode().say_my_name_and_more(name="joey hendricks")

# Generate Flame Graph
FlameGraphs().export_flame_graph(path="C:\\Temp\\")
```
Using the pattern shown above you can run your function and quickly pull out a flame graph to 
view where your performance bottleneck is situated. 
The example code would generate the following flame graph:

[![Example of simple flame graph](/images/fancy_code_flame_graph.svg "flame graph simple")](
https://raw.githubusercontent.com/JoeyHendricks/python-unit-level-performance-testing/95132b0a0ebd61f57deb7ec2197d01e5c0d4829f/images/fancy_code_flame_graph.svg)

> Image is interactive



## Options

QuickPotato comes equipped with some options you can configure to make sure QuickPotato fits your needs.
Below you can find a list of all options and what they can do:

```python
from QuickPotato.configuration.management import options

# Profiling Settings
options.enable_intrusive_profiling = True 
options.enable_system_resource_collection = True

# Results Storage
options.connection_url = None  # <-- None will use SQlite and store results in Temp directory
options.enable_database_echo = False

# Storage Maintenance 
options.enable_auto_clean_up_old_test_results = True
options.maximum_number_of_saved_test_results = 10

```

> Do note that the states of options are saved in a static yaml options file.  
> That is why settings can be defined just once or changed on the fly. 

### Boundary Testing

Within QuickPotato, it is possible to create a performance test that validates if 
your code breaches any defined boundary or not.
An example of this sort of test can be found in the snippet below: 

```python
from QuickPotato.profiling.intrusive import unit_performance_test as upt
from QuickPotato.harness.export import PerformanceStatisticsExport
from demo.example_code import fast_method

upt.test_case_name = "test_performance"  # <-- Define test case name
upt.max_and_min_boundary_for_average = {"max": 1, "min": 0.001}  # <-- Establish performance boundaries

# Execute method under test
for _ in range(0, 10):
    fast_method()

# Analyse profiled results will output True if boundaries are not breached otherwise False
results = upt.verify_benchmark_against_set_boundaries

# Export time spent statistical to csv
if results is False:
    TimeSpentStatisticsExport(
        test_case_name=upt.test_case_name,
        test_id=upt.current_test_id,
        delimiter=";",
        path="C:\\Temp\\",
        purge_database_after_export=True  # <-- Optionally clean-up the database after use.
    ).to_csv()

```
### Regression Testing

Besides testing if your code does not breach any boundaries, it is also possible to verify that there is no regression 
between the current benchmark and a previous baseline.
The method for creating such a test can be found in the snippet below.

```python
from QuickPotato.profiling.intrusive import unit_performance_test as upt
from QuickPotato.harness.export import PerformanceStatisticsExport
from demo.example_code import fast_method


upt.test_case_name = "test_performance"  # <-- Define test case name

# Execute method under test
for _ in range(0, 10):
    fast_method()

# Analyse results for change True if there is no change otherwise False
results = upt.verify_benchmark_against_previous_baseline

# Export time spent statistical to csv
if results is False:
    TimeSpentStatisticsExport(
        test_case_name=upt.test_case_name,
        test_id=upt.current_test_id,
        delimiter=";",
        path="C:\\Temp\\"
    ).to_csv()

```

## Read More About Unit Performance Testing

If you want to learn more about unit-level performance testing then check out the following resources:

[Don’t lose your mind over slow code check your performance sanity.](https://www.linkedin.com/pulse/dont-lose-your-mind-over-slow-code-check-performance-sanity-joey/) 
