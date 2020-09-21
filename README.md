[![Couch Potato code in a lazy chair](/images/potato-banner-tv.jpg "Slow Potato Code")](https://github.com/JoeyHendricks/python-low-level-performance-testing/blob/master/images/potato-banner-tv.png?raw=true)

## Building low level performance tests for Python with QuickPotato

QuickPotato is a low level performance testing framework that helps you gets rid of slow couch potato code.
It allows you to verify if the performance of your code is working like expected 
by being able to answer the following two questions:

- Is my code performing in the way I am expecting?
- Did this code change deteriorate the performance of my code or project?

It is then possible to get the answers of these two question on the following two levels:

1. The smallest unit.
2. Multiple units that make up a piece of functionality.

> To what extend you want your performance tests to interact with stubs completely 
> depends on how effortless you can spin up production-like environments. 

The cool thing about QuickPotato is that it provides you with all the tools needed to 
answer these two important questions in a easy, reliable, and completely automated way. 
By creating automated low level performance tests with QuickPotato, you are automatically 
doing the following things:

- Measuring the end to end performance of your code.
- Profiling your code with CProfile.
- Collecting system resource utilization.
- Automated decisions about the performance of your code. 

By removing as many obstacles between you and performance testing your code.
QuickPotato hopes to enable you to get fast feedback about the speed of your code.
Giving you the space to focus on delivering awesome code which is lighting fast! 

## How it works

### Installation

Install using [pip](https://pip.pypa.io/en/stable/) or download the source code from GitHub.
```bash
pip install QuickPotato
```

### Intrusive Testing

Not all functions hold the same risk of forming a potential performance problem like others.
Therefore it is possible with QuickPotato to pick and choose which function should be measured and profiled.

The chosen functions need to be fitted with a performance_critical decorator so QuickPotato knows that this
function needs to be tested when triggered during a unit performance test. 
The snippet below gives you a example of how you can decorate function for use with QuickPotato.

```python
from QuickPotato.inspect.intrusive import performance_critical


@performance_critical
def example():
    return 1 + 1

```

It is important to understand that when using the intrusive method. 
That there are no side effect when during normal operation.

### Boundary Testing

Within QuickPotato it is possible to create a performance test that validates if 
your code does not breach any defined boundary.
An example of this sort of test can be found in the snippet below: 

```python
from QuickPotato.inspect.intrusive import unit_performance_test
from example.intrusive_example import example

# Setup your unit performance test.
upt = unit_performance_test
upt.test_case_name = "Default"

# Define the boundaries for your code.
upt.max_and_min_boundary_for_average = {"max": 0.200, "min": 0.011}
        
# Run functions which are decorated as performance critical.
for _ in range(0, 10):
    example() # <-- Your function or class here.
        
# Verify if the function does not breach any defined boundaries.
results = upt.verify_if_benchmark_does_not_breach_defined_boundaries()
```
### Regression Testing

Besides testing if your code does not breach any boundaries.
It is also possible to verify that there is no regression between the current benchmark and a previous baseline.
How to create such a test can be found in the snippet below.

```python
from QuickPotato.inspect.intrusive import unit_performance_test
from example.intrusive_example import example

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