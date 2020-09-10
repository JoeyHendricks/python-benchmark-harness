## Start creating low level performance tests with QuickPotato

Uplift the way you tste

QuickPotato is a library that enables developer to create automated unit or component level performance tests.

 

So what is a performance sanity check? Well, it is a test to quickly evaluate if the code on a unit level has the expected performance behaviour within a reliable testing environment.

It is then possible to answer two primary questions with these sanity checks - Does the performance overstep the set thresholds? How much regression is there between the old method and the newly written method?

If these performance sanity checks pass, then we know that the performance of the code meets our expectations. On the other hand, if they fail, then we know that the performance has deteriorated.

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install QuickPotato.

```bash
pip install QuickPotato
```

### Intrusive Testing


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