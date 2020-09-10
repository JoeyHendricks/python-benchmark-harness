## Building low level performance tests for Python

With QuickPotato it is possible to create automated low level performance tests 
that gather as much information about your code as possible. 
Allowing you to verify if the performance of your code is working like expected 
and answer the following two questions:

- Is my code performing in the way I am expecting?
- Did this code change deteriorate the performance of my code or project?

QuickPotato provides you with the tools needed to answer these two important 
questions in a easy, reliable, and automated way. Making sure that you can focus
on delivering awesome code that is lighting fast! 

## How it works




> 

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