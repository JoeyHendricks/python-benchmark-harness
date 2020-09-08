## QuickPotato

A library that helps automate performance tests on the unit level.

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install QuickPotato.

```bash
pip install QuickPotato
```

### Intrusive Profiling Usage

QuickPotato support intrusive profiling this means that only methods that are marked with a decorator are tested.
This enables you to pick and choose which methods you want to measure and validate in your performance unit test.
Besides that it also empathizes which methods are potential performance risk.
So team members know that this method is sensitive for performance problems.

Below you can find instruction how to set-up a unit performance test with QuickPotato:  

```python
from QuickPotato.inspect.intrusive import performance_critical # <-- Decorator 
from QuickPotato.inspect.intrusive import unit_performance_test # <-- Testing Object
import unittest # <-- The unit test framework 

# Step 1. Mark performance critical methods with a QuickPotato decorator
@performance_critical
def foo(y):
    x = y + 1 
    return x

class ValidatePerformanceOfProject(unittest.TestCase):

    # Step 2. Define a performance unit test like below
    def test_foo_for_performance(self):
        
        # Step 3. Define your test case name, metric boundaries or statistical regression tests 
        unit_performance_test.test_case_name = "Test Case Name Here!"
    
        # Example: for setting boundaries for the overall average response time
        # max and min key = Either Float or Integer to not validate boundary use None
        unit_performance_test.max_and_min_boundary_for_average = {"max": 1, "min": None}
    
        # Example: Turn on statistical regression tests
        # True = Execute Test, False = Skip Test
        unit_performance_test.regression_setting_perform_f_test = True
        unit_performance_test.regression_setting_perform_t_test = True
        
        # Execute method a couple times to collect metrics
        for _ in range(0, 10): # <-- Make sure your sample size is higher then 10
            foo(y=7)
        
        # Step 4. Run your verifications and bind the results to a variable  
        regression_tests = unit_performance_test.analyse_benchmark_against_baseline_for_regression()
        threshold_tests = unit_performance_test.analyse_benchmark_against_defined_boundaries()
        
        # Step 5. Validate the output with the unit test framework
        self.assertIsNone(regression_tests) # <-- Is None on first use because there is NO BASELINE
        self.assertTrue(threshold_tests)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Read More About Unit Performance Testing

My LinkedIn article describing the concept with all it benefits and problems.
[Don’t lose your mind over slow code check your performance sanity.](https://www.linkedin.com/pulse/dont-lose-your-mind-over-slow-code-check-performance-sanity-joey/) 