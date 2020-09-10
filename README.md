## Building low level performance tests for Python with QuickPotato

QuickPotato is a low level performance testing framework that helps you gets rid of slow couch potato code.
It allows you to verify if the performance of your code is working like expected 
by being able to answer the following two questions:

- Is my code performing in the way I am expecting?
- Did this code change deteriorate the performance of my code or project?

It is then possible to get the answers of these two question on the following two levels:

1. The smallest unit.
2. Multiple units that make up a piece of functionality.

> To what extend you want to stub level on each level completely depends on how effortless 
you can spin up production-like environments. 

The cool thing about QuickPotato is that it provides you with all the tools needed to 
answer these two important questions in a easy, reliable, and completely automated way. 
By creating automated low level performance tests with QuickPotato, you are automatically 
doing the following things:

- Measuring the end to end performance of your code.
- Profiling your code with CProfile.
- Collecting system resource utilization.
- make automated decisions about the performance of your code. 

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
function needs to be tested when executed during a unit performance test.
The snippet below gives you a example of how you can decorate function for use with QuickPotato.

```python
from QuickPotato.inspect.intrusive import performance_critical


@performance_critical
def example():
    return 1 + 1

```




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
results = upt.analyse_benchmark_against_defined_boundaries()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Read More About Unit Performance Testing

My LinkedIn article describing the concept with all it benefits and problems.
[Don’t lose your mind over slow code check your performance sanity.](https://www.linkedin.com/pulse/dont-lose-your-mind-over-slow-code-check-performance-sanity-joey/) 