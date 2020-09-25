[![Couch Potato code in a lazy chair](/images/potato-banner-tv.jpg "Slow Potato Code")](https://github.com/JoeyHendricks/python-low-level-performance-testing/blob/master/images/potato-banner-tv.png?raw=true)


## Building unit level performance tests for Python with QuickPotato

QuickPotato is unit-level performance testing framework for the Python programming language. 
Enabling its user to define helpful test cases which can help catch problematic performance bottlenecks 
in the early stages of the development life cycle.

It does by helping you answer two burning questions about your code. 

- Did that code change just impact the performance?
- Is my code performing in the way which I am expecting?

Getting answers to these questions is not always easy. 
That is why QuickPotato aims to equip you with all the tools necessary to get the job done. 
What QuickPotato has in its growing arsenal boils down to the following features:

- Measure the end to end performance of your code.
- Automatically profile your code with CProfile.
- Collect system resource utilization during execution.
- Automatically discover performance regression after a code change. 
- Verify if your code does not breach any performance boundaries.

QuickPotato hopes to remove as many obstacles between you and performance testing your code. 
Allowing you to quickly fix the problem at hand continue creating awesome projects!

## How it works

### Installation

Install using [pip](https://pip.pypa.io/en/stable/) or download the source code from GitHub.
```bash
pip install QuickPotato
```
(Due note that QuickPotato is not yet released)

### Intrusive Testing

Using QuickPotato's intrusive performance testing method requires you to decorate your function. 
By tagging your function With the "performance_critical" decorator you are providing 
QuickPotato access to profile this function.  

Besides that QuickPotato technically needs "performance_critical" decorator to be able to work. 
It also serves a human purpose be decorating functions as performance-critical. 
You are reminding your self and your teammates to think about the performance of the code.
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

Once you import and attach the "performance_critical" decorator to your function you are two steps
away of gaining insights into the performance of your code. 
The code snippet below shows you the final two step needed to get performance statistics out of your code: 

```python
from demo.example_of_slow_and_fast_functions import *
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

```
> Do note that the states of options are saved in a static yaml options file.  

### Boundary Testing

Within QuickPotato it is possible to create a performance test that validates if 
your code does not breach any defined boundary.
An example of this sort of test can be found in the snippet below: 

```python
from QuickPotato.inspect.intrusive import unit_performance_test as upt
from QuickPotato.configuration.manager import options
from QuickPotato.harness.export import TimeSpentStatisticsExport
from demo.example_of_slow_and_fast_functions import fast_method

upt.test_case_name = "verify_performance_of_fast_method"  # <-- Define test case name
upt.max_and_min_boundary_for_average = {"max": 1, "min": 0.001}  # <-- Establish performance boundaries

options.enable_intrusive_profiling = True  # <-- Set to True to enable profiling

# Execute method under test
for _ in range(0, 10):
    fast_method()

# Analyse profiled results will output True if boundaries are not breached otherwise False
results = upt.verify_if_benchmark_does_not_breach_defined_boundaries()

options.enable_intrusive_profiling = False  # <-- Set to False to disable profiling

# Export time spent statistics to csv
TimeSpentStatisticsExport(
    test_case_name=upt.test_case_name,
    test_id=upt.current_test_id,
    delimiter=";",
    path="C:\\Temp\\",
    purge_database_after_export=True  # <-- Optionally clean-up the database after use.
).to_csv()

```
### Regression Testing

Besides testing if your code does not breach any boundaries.
It is also possible to verify that there is no regression between the current benchmark and a previous baseline.
How to create such a test can be found in the snippet below.

```python
from QuickPotato.inspect.intrusive import unit_performance_test
from demo.intrusive_example import example

# Setup your unit performance test.
upt = unit_performance_test
upt.test_case_name = "Default"
upt.regression_setting_perform_f_test = True
upt.regression_setting_perform_t_test = True

# Run functions which are decorated as performance critical.
for _ in range(0, 10):
    example() # <-- Your function or class here.

# Verify if the function does not contain any change.
results = upt.verify_that_there_is_no_change_between_the_baseline_and_benchmark()
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Read More About Unit Performance Testing

If you want to learn more about low level performance testing than check out the following resources:

[Don’t lose your mind over slow code check your performance sanity.](https://www.linkedin.com/pulse/dont-lose-your-mind-over-slow-code-check-performance-sanity-joey/) 
