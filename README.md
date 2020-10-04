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
> you can find a wheel file under the distribution folder to install it with. 

### Intrusive Testing

Using QuickPotato's intrusive performance testing method requires you to decorate your function. 
By tagging your function with the "performance_critical" decorator, you are providing QuickPotato access to profile this function.  

Besides that, QuickPotato technically needs "performance_critical" decorator to be able to work. 
It also serves a human purpose of decorating functions as performance-critical. 
Thus, you remind yourself and your teammates to think about the performance of the code.
An example of this concept can be found below:

```python
from QuickPotato.inspect.intrusive import performance_critical  # <-- Import the decorator
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

Once you import and attach the "performance_critical" decorator to your function, you are just a few steps
away from gaining insights into the performance of your code. 
The code snippet below, shows you the basics you need to know to get the performance statistics out of your code: 

```python
from demo.example_code import *
from QuickPotato.configuration.management import options  # <-- Import the options object
from QuickPotato.harness.export import TimeSpentStatisticsExport


options.enable_intrusive_profiling = True  # <-- Set to True to enable profiling

fast_method()

options.enable_intrusive_profiling = False  # <-- Set to False to disable profiling

# Export all results to csv
TimeSpentStatisticsExport(
    path="C:\\Temp\\",
    purge_database_after_export=True  # <-- Optionally clean-up the database after use.
).to_csv()

```

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
from QuickPotato.inspect.intrusive import unit_performance_test as upt
from QuickPotato.harness.export import TimeSpentStatisticsExport
from demo.example_code import fast_method

upt.test_case_name = "test_performance"  # <-- Define test case name
upt.max_and_min_boundary_for_average = {"max": 1, "min": 0.001}  # <-- Establish performance boundaries

# Execute method under test
for _ in range(0, 10):
    fast_method()

# Analyse profiled results will output True if boundaries are not breached otherwise False
results = upt.verify_benchmark_against_set_boundaries

# Export time spent statistics to csv
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
from QuickPotato.inspect.intrusive import unit_performance_test as upt
from QuickPotato.harness.export import TimeSpentStatisticsExport
from demo.example_code import fast_method


upt.test_case_name = "test_performance"  # <-- Define test case name

# Execute method under test
for _ in range(0, 10):
    fast_method()

# Analyse results for change True if there is no change otherwise False
results = upt.verify_benchmark_against_previous_baseline

# Export time spent statistics to csv
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
